import boto3
import yaml
import requests
import math

with open("variants.yaml", "r") as fi:
    variants = yaml.safe_load(fi)

unit_list = list(zip(['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'], [0, 0, 1, 2, 2, 2]))
def sizeof_fmt(num):
    """Human friendly file size"""
    if num > 1:
        exponent = min(int(math.log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024**exponent
        unit, num_decimals = unit_list[exponent]
        format_string = '{:.%sf} {}' % (num_decimals)
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'


# Retrieve the list of existing buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
# print('Existing buckets:')
# for bucket in response['Buckets']:
#     print(f'  {bucket["Name"]}')

SHA_MARKER = "===SHA 256 SUMS===\n\n"
s3 = boto3.resource('s3')
bucket = s3.Bucket('conda-uploads')
for v in variants["build_variants"]:
    print(f"\n\nVariant: {v}")
    print("-" * len(f"Variant: {v}") + "\n")
    log = None
    for object_summary in bucket.objects.filter(Prefix=f'tensorflow-2/{v}'):
        url = f'https://{bucket.name}.s3.amazonaws.com/{object_summary.key}'
        fname = url.rsplit('/', 1)[-1]
        fsize = sizeof_fmt(object_summary.size)

        object_summary.Acl().put(ACL='public-read')
        print(f"- [`{fname}`]({url}) ({fsize})")
        if url.endswith('log'):
            log = url

    if log:
        response = requests.get(log)
        log_content = response.content.decode('utf-8')
        idx = log_content.find(SHA_MARKER)
        shasums = log_content[idx + len(SHA_MARKER):]

        print("\n**SHA256 sums**\n")
        print(f"```\n{shasums}```")

