from fpdf import FPDF

def create_sample_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    text = """
    Acme Corp Customer Support Knowledge Base
    
    1. Refund Policy:
    Customers can request a refund within 30 days of purchase. The item must be in its original condition.
    To process a refund, please email support@acmecorp.com with your order number.
    
    2. Subscription Cancellation:
    To cancel your subscription, go to your account settings, click on 'Billing', and select 'Cancel Subscription'.
    Your subscription will remain active until the end of the current billing cycle.
    
    3. Shipping Information:
    Standard shipping takes 3-5 business days. Expedited shipping takes 1-2 business days.
    Free shipping is available on orders over $50.
    """
    
    pdf.multi_cell(0, 10, text)
    pdf.output("sample_knowledge.pdf")
    print("Created 'sample_knowledge.pdf' successfully!")

if __name__ == "__main__":
    create_sample_pdf()
