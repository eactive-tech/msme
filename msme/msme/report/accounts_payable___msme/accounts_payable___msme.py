# Copyright (c) 2025, Gautam Tyagi and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}
    
    Invoice_details = frappe.call(
        "frappe.desk.query_report.run",
        report_name="Accounts Payable",
        filters=filters,
        ignore_prepared_report=True
    )

    # Custom Columns
    Invoice_details["columns"].insert(3, {'label': 'Enterprise Type', 'fieldname': 'custom_enterprise_type', 'fieldtype': 'Data'})
    Invoice_details["columns"].insert(4, {'label': 'Registration Date', 'fieldname': 'custom_udyam_registration_date', 'fieldtype': 'Data'})
    Invoice_details["columns"].insert(5, {'label': 'Udyam Registration Number', 'fieldname': 'custom_udyam_registration_number', 'fieldtype': 'Data'})
    Invoice_details["columns"].insert(6, {'label': 'Business Category', 'fieldname': 'custom_business_category', 'fieldtype': 'Data'})

    
    if Invoice_details.get("result"):
        Invoice_details["result"].pop()

    if not Invoice_details.get("result"):
        return Invoice_details["columns"], []

    filtered_result = []

    for x in Invoice_details["result"]:
        if x.get("party_type") == "Supplier":

            is_msme_registered = frappe.db.get_value("Supplier", x.get("party"), "custom_is_msme_registered")

            if is_msme_registered == 1:
                x["custom_enterprise_type"] = frappe.db.get_value("Supplier", x.get("party"), "custom_enterprise_type") or ""
                x["custom_udyam_registration_date"] = frappe.db.get_value("Supplier", x.get("party"), "custom_udyam_registration_date") or ""
                x["custom_udyam_registration_number"] = frappe.db.get_value("Supplier", x.get("party"), "custom_udyam_registration_number") or ""
                x["custom_business_category"] = frappe.db.get_value("Supplier", x.get("party"), "custom_business_category") or ""
                
                filtered_result.append(x)

    return Invoice_details["columns"], filtered_result
