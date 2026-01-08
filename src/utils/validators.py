"""
Validation utilities for the Retail Order Query Chatbot.
"""

import re
from typing import Tuple, Optional


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email address.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, None


def validate_order_id(order_id: str) -> Tuple[bool, Optional[str]]:
    """
    Validate order ID format.
    
    Args:
        order_id: Order ID to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not order_id:
        return False, "Order ID is required"
    
    # Common order ID patterns
    patterns = [
        r'^ORD-\d+$',           # ORD-12345
        r'^#\d+$',              # #12345
        r'^\d{5,12}$',          # 12345
        r'^[A-Z]{2,3}-\d+$',    # AB-12345
    ]
    
    for pattern in patterns:
        if re.match(pattern, order_id.upper()):
            return True, None
    
    return False, "Invalid order ID format"


def validate_coupon_code(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate coupon code format.
    
    Args:
        code: Coupon code to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not code:
        return False, "Coupon code is required"
    
    if len(code) < 3:
        return False, "Coupon code is too short"
    
    if len(code) > 20:
        return False, "Coupon code is too long"
    
    if not re.match(r'^[A-Za-z0-9]+$', code):
        return False, "Coupon code must be alphanumeric"
    
    return True, None


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """
    Validate phone number.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone:
        return False, "Phone number is required"
    
    digits = re.sub(r'\D', '', phone)
    
    if len(digits) < 10:
        return False, "Phone number must have at least 10 digits"
    
    if len(digits) > 15:
        return False, "Phone number is too long"
    
    return True, None


def validate_zip_code(zip_code: str, country: str = "US") -> Tuple[bool, Optional[str]]:
    """
    Validate ZIP/postal code.
    
    Args:
        zip_code: ZIP code to validate
        country: Country code
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not zip_code:
        return False, "ZIP code is required"
    
    patterns = {
        "US": r'^\d{5}(-\d{4})?$',
        "CA": r'^[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d$',
        "UK": r'^[A-Za-z]{1,2}\d[A-Za-z\d]?\s?\d[A-Za-z]{2}$',
    }
    
    pattern = patterns.get(country.upper(), patterns["US"])
    
    if not re.match(pattern, zip_code):
        return False, f"Invalid ZIP code format for {country}"
    
    return True, None


def validate_product_quantity(quantity: int) -> Tuple[bool, Optional[str]]:
    """
    Validate product quantity.
    
    Args:
        quantity: Quantity to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if quantity < 0:
        return False, "Quantity cannot be negative"
    
    if quantity > 100:
        return False, "Maximum quantity is 100"
    
    return True, None


def validate_rating(rating: float) -> Tuple[bool, Optional[str]]:
    """
    Validate product rating.
    
    Args:
        rating: Rating to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if rating < 0:
        return False, "Rating cannot be negative"
    
    if rating > 5:
        return False, "Rating cannot exceed 5"
    
    return True, None


def sanitize_search_query(query: str) -> str:
    """
    Sanitize search query.
    
    Args:
        query: Raw search query
        
    Returns:
        Sanitized query
    """
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\';]', '', query)
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    # Limit length
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    return sanitized
