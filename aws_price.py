import boto3
import json


def filter_ec2s(region, instance, os):
    EC2_Filters = [
        {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": os},
        {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance},
        {"Type": "TERM_MATCH", "Field": "location", "Value": region},
        {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "shared"},
    ]
    return EC2_Filters


def get_price(region, instance, os):
    client = boto3.client("pricing")
    products = client.get_products(
        ServiceCode="AmazonEC2",
        Filters=filter_ec2s(region, instance, os),
        MaxResults=100,
    )

    ec2_products = json.loads(products["PriceList"][0])["terms"]["OnDemand"]
    ec2_product = list(ec2_products)[0]
    price_dimensions = list(ec2_products[ec2_product]["priceDimensions"])[0]
    return ec2_products[ec2_product]["priceDimensions"][price_dimensions][
        "pricePerUnit"
    ]["USD"]


def get_region_name(region_code):
    client = boto3.client("ssm")

    response = client.get_parameter(
        Name="/aws/service/global-infrastructure/regions/%s/longName" % region_code
    )

    region_name = response["Parameter"]["Value"]
    return region_name
