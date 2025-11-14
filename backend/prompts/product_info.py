"""
EliseAI Product Information
Core product descriptions for the AI SDR to reference.
"""

PRODUCTS = {
    "LeasingAI": {
        "name": "LeasingAI",
        "tagline": "24/7 AI Leasing Assistant",
        "description": "An AI assistant that handles prospect inquiries 24/7, schedules tours, answers questions about pricing and amenities, and helps boost lead-to-lease rates.",
        "key_features": [
            "24/7 prospect inquiry handling",
            "Automated tour scheduling",
            "Pricing and amenity information",
            "Lead qualification",
            "Increased lead-to-lease conversion"
        ],
        "ideal_for": "Property management companies looking to improve leasing efficiency and capture more leads"
    },
    "MaintenanceAI": {
        "name": "MaintenanceAI",
        "tagline": "AI-Powered Maintenance Workflow",
        "description": "Streamlines the maintenance workflow through AI-powered technician assignment, work order management, and integration with property management systems.",
        "key_features": [
            "Automated technician assignment",
            "Smart work order management",
            "Property management system integration",
            "Workflow optimization",
            "Reduced response times"
        ],
        "ideal_for": "Operations teams managing high volumes of maintenance requests"
    },
    "DelinquencyAI": {
        "name": "DelinquencyAI",
        "tagline": "Automated Payment Management",
        "description": "Automatically sends payment reminders, follows up on outstanding payments, and helps reduce delinquency rates.",
        "key_features": [
            "Automated payment reminders",
            "Intelligent follow-up sequences",
            "Delinquency rate reduction",
            "Personalized communication",
            "Payment plan management"
        ],
        "ideal_for": "Property managers focused on improving collections and cash flow"
    },
    "LeaseAudits": {
        "name": "LeaseAudits",
        "tagline": "Automated Lease Compliance",
        "description": "Helps ensure lease compliance and accuracy through automated review processes.",
        "key_features": [
            "Automated lease review",
            "Compliance checking",
            "Error detection",
            "Risk mitigation",
            "Audit trail documentation"
        ],
        "ideal_for": "Legal and compliance teams managing large portfolios"
    },
    "EliseCRM": {
        "name": "EliseCRM",
        "tagline": "AI-First Real Estate CRM",
        "description": "A comprehensive CRM platform that serves as a hub for prospect and resident information, reporting, and operational workflows.",
        "key_features": [
            "Centralized prospect and resident data",
            "Advanced reporting and analytics",
            "Operational workflow management",
            "Integration with all EliseAI products",
            "Customizable dashboards"
        ],
        "ideal_for": "Property management companies looking for a centralized operations hub"
    }
}


def get_product_overview() -> str:
    """Get a formatted overview of all products for the system prompt."""
    overview = "## EliseAI Products\n\n"
    
    for product_id, product in PRODUCTS.items():
        overview += f"### {product['name']}: {product['tagline']}\n"
        overview += f"{product['description']}\n\n"
        overview += "Key Features:\n"
        for feature in product['key_features']:
            overview += f"- {feature}\n"
        overview += f"\nIdeal for: {product['ideal_for']}\n\n"
    
    return overview


def get_product_names() -> list[str]:
    """Get list of all product names."""
    return list(PRODUCTS.keys())

