"""
Formatting utilities for the Retail Order Query Chatbot.
"""

from datetime import datetime, date
from typing import Optional


def format_price(amount: float, currency: str = "USD") -> str:
    """
    Format a price amount.
    
    Args:
        amount: Price amount
        currency: Currency code
        
    Returns:
        Formatted price string
    """
    symbols = {"USD": "$", "EUR": "€", "GBP": "£", "CAD": "C$"}
    symbol = symbols.get(currency, "$")
    return f"{symbol}{amount:,.2f}"


def format_date(
    date_input: str | date | datetime,
    style: str = "medium"
) -> str:
    """
    Format a date for display.
    
    Args:
        date_input: Date to format
        style: Format style (short, medium, long)
        
    Returns:
        Formatted date string
    """
    if isinstance(date_input, str):
        try:
            parsed = datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            return date_input
    elif isinstance(date_input, datetime):
        parsed = date_input
    elif isinstance(date_input, date):
        parsed = datetime.combine(date_input, datetime.min.time())
    else:
        return str(date_input)
    
    formats = {
        "short": "%m/%d/%y",
        "medium": "%b %d, %Y",
        "long": "%B %d, %Y",
    }
    
    return parsed.strftime(formats.get(style, formats["medium"]))


def format_order_status(status: str) -> str:
    """
    Format order status with emoji.
    
    Args:
        status: Raw status string
        
    Returns:
        Formatted status with emoji
    """
    status_map = {
        "pending": "⏳ Pending",
        "processing": "📋 Processing",
        "shipped": "📦 Shipped",
        "in_transit": "🚚 In Transit",
        "out_for_delivery": "🏃 Out for Delivery",
        "delivered": "✅ Delivered",
        "cancelled": "❌ Cancelled",
        "returned": "↩️ Returned",
        "refunded": "💰 Refunded",
    }
    return status_map.get(status.lower(), status)


def format_product_price(
    price: float,
    sale_price: Optional[float] = None
) -> str:
    """
    Format product price with optional sale price.
    
    Args:
        price: Original price
        sale_price: Sale price if on sale
        
    Returns:
        Formatted price string
    """
    if sale_price and sale_price < price:
        discount = int((1 - sale_price / price) * 100)
        return f"~~${price:.2f}~~ **${sale_price:.2f}** ({discount}% off)"
    return f"${price:.2f}"


def format_stock_status(quantity: int) -> str:
    """
    Format stock status.
    
    Args:
        quantity: Stock quantity
        
    Returns:
        Formatted stock status
    """
    if quantity == 0:
        return "❌ Out of Stock"
    elif quantity <= 3:
        return f"⚠️ Low Stock ({quantity} left)"
    elif quantity <= 10:
        return f"🟡 Limited Stock ({quantity} available)"
    else:
        return "✅ In Stock"


def format_rating(rating: float, max_rating: float = 5.0) -> str:
    """
    Format rating with stars.
    
    Args:
        rating: Rating value
        max_rating: Maximum rating
        
    Returns:
        Formatted rating with stars
    """
    full_stars = int(rating)
    half_star = rating - full_stars >= 0.5
    empty_stars = int(max_rating) - full_stars - (1 if half_star else 0)
    
    stars = "⭐" * full_stars
    if half_star:
        stars += "✨"
    
    return f"{stars} {rating:.1f}/5"


def format_shipping_estimate(days: int) -> str:
    """
    Format shipping estimate.
    
    Args:
        days: Number of days
        
    Returns:
        Formatted shipping estimate
    """
    if days == 0:
        return "📦 Same-day delivery"
    elif days == 1:
        return "🚀 Next-day delivery"
    elif days <= 3:
        return f"⚡ {days} business days"
    else:
        return f"📬 {days} business days"


def format_cart_summary(
    subtotal: float,
    tax: float,
    shipping: float,
    discount: float,
    total: float
) -> str:
    """
    Format cart summary.
    
    Args:
        subtotal: Subtotal amount
        tax: Tax amount
        shipping: Shipping cost
        discount: Discount amount
        total: Total amount
        
    Returns:
        Formatted cart summary
    """
    lines = [
        f"Subtotal: {format_price(subtotal)}",
        f"Tax: {format_price(tax)}",
    ]
    
    if shipping > 0:
        lines.append(f"Shipping: {format_price(shipping)}")
    else:
        lines.append("Shipping: FREE 🎉")
    
    if discount > 0:
        lines.append(f"Discount: -{format_price(discount)} 💰")
    
    lines.append(f"**Total: {format_price(total)}**")
    
    return "\n".join(lines)
