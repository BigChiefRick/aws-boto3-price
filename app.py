from aws_price import get_price, get_region_name

total_price = get_price(get_region_name('us-west-1'), 't3.micro', 'linux')

print('total price of EC2 instance, ' total_price)
