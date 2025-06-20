from itertools import combinations
from collections import defaultdict
import requests
import os

def download_document(file_name, document_url):
   if os.path.exists(file_name):
       pass
   else:
       response = requests.get(document_url)
       if response.status_code == 200:
           with open(file_name, 'wb') as f:
               f.write(response.content)
       else:
           print(f'Failed to download the document. Status code: {response.status_code}')



def read_orders_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip().split('@@@') for line in f if line.strip()]


def count_products_and_pairs(orders):
    product_count = defaultdict(int)
    pair_count = defaultdict(int)

    for order in orders:
        unique_items = set(order)
        for item in unique_items:
            product_count[item] += 1
        for product_one, product_two in combinations(sorted(unique_items), 2):
            pair_count[(product_one, product_two)] += 1

    return product_count, pair_count


def calculate_confidence_and_filter(product_count, pair_count, support_threshold, confidence_threshold):
    results = []

    for (item1, item2), support in pair_count.items():
        if support < support_threshold:
            continue

        conf1 = support / product_count[item1]
        conf2 = support / product_count[item2]

        if conf1 >= confidence_threshold:
            results.append((item1, item2, conf1, support))

        if conf2 >= confidence_threshold:
            results.append((item2, item1, conf2, support))

    return results


def print_results(results):
    for idx, (A, B, confidence, support) in enumerate(results, 1):
        print(f"p{idx} {A} => {B} ({confidence * 100:.2f}% confidence), {support} support")


def main():
    filename = 'orders.txt'
    support_threshold = 15
    confidence_threshold = 0.45

    orders = read_orders_from_file(filename)
    product_count, pair_count = count_products_and_pairs(orders)
    filtered_results = calculate_confidence_and_filter(
        product_count, pair_count, support_threshold, confidence_threshold
    )
    print_results(filtered_results)


if __name__ == "__main__":
    file_name = 'orders.txt'
    document_url = 'https://drive.google.com/uc?id=1IOPTVq2ooQfZRkF3rAjGkTjRtbotG7FF'
    download_document(file_name, document_url)
    main()
