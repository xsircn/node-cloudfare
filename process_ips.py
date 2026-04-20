import requests
from ipwhois import IPWhois
import os

# 定义你关心的 ASN 映射 (示例)
# 格式为 'ASN编号': '存储文件名'
ASN_TARGETS = {
    '13238': 'CNMC',      # 中国移动
    '4837': 'CNUC',       # 中国联通
    '4134': 'CNTL',       # 中国电信
    '13335': 'CLOUDFLARE' # Cloudflare 自身的节点
}

def get_cloudflare_ips():
    response = requests.get("https://www.cloudflare.com/ips-v4")
    return response.text.strip().split('\n')

def get_asn(ip_cidr):
    try:
        # 取 CIDR 的第一个 IP 进行查询
        ip = ip_cidr.split('/')[0]
        obj = IPWhois(ip)
        results = obj.lookup_rdap(depth=1)
        return str(results.get('asn'))
    except Exception as e:
        print(f"Error checking {ip_cidr}: {e}")
        return None

def main():
    ips = get_cloudflare_ips()
    # 建立一个字典存储分类结果
    results = {name: [] for name in ASN_TARGETS.values()}
    results['Others'] = []

    for cidr in ips:
        asn = get_asn(cidr)
        name = ASN_TARGETS.get(asn, 'Others')
        results[name].append(cidr)
        print(f"IP: {cidr} -> ASN: {asn} ({name})")

    # 写入文件
    for name, cidr_list in results.items():
        if cidr_list:
            with open(f"CF-{name}.txt", "w") as f:
                f.write('\n'.join(cidr_list))

if __name__ == "__main__":
    main()
