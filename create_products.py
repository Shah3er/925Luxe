import stripe

stripe.api_key = "sk_test_51RKOjYFLy2fLmwrk9xXGnIRn0zH1YvClcIajMda1ySNOYDqAA7FBz0JkuHHHXiZorSfwSl5ldfVIxbJ0MWSH5glQ00b8nl6ThV"

# Stripe Product ID for Cuban Link Chain
cuban_chain_product_id = "prod_SHVaYPi6wFwyMe"  # Replace with your actual Product ID

# Pricing table based on length only (width is fixed at 14mm)
cuban_chain_pricing = {
    "16": 6000,
    "18": 6200,
    "20": 6400,
    "22": 6600,
    "24": 6800,
}

for length, price in cuban_chain_pricing.items():
    nickname = f"{length}\" - 14mm"
    created_price = stripe.Price.create(
        unit_amount=price,
        currency="cad",
        product=cuban_chain_product_id,
        nickname=nickname,
    )
    print(f"Created Price for {nickname}: {created_price.id}")
