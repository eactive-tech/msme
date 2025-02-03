# Copyright (c) 2025, Gautam Tyagi and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    company = filters.get("company")
    report_date = filters.get("report_date")
    finance_book = filters.get("finance_book")
    cost_center = filters.get("cost_center")
    party_account = filters.get("party_account")
    ageing_based_on = filters.get("ageing_based_on")
    range = filters.get("range")
    payment_terms_template = filters.get("payment_terms_template")
    party_type = filters.get("party_type")
    party = filters.get("party")
    supplier_group = filters.get("supplier_group")
    group_by_party = filters.get("group_by_party")
    based_on_payment_terms = filters.get("based_on_payment_terms")
    show_remarks = filters.get("show_remarks")
    show_future_payments = filters.get("show_future_payments")
    in_party_currency = filters.get("in_party_currency")
    for_revaluation_journals = filters.get("for_revaluation_journals")
    ignore_accounts = filters.get("ignore_accounts")
    handle_employee_advances = filters.get("handle_employee_advances")

    
    Invoice_details = frappe.call(
        "frappe.desk.query_report.run",
        report_name="Accounts Payable",
        filters={
            "company": company,
            "report_date": report_date,
            "finance_book": finance_book,
            "cost_center": cost_center,
            "party_account": party_account,
            "ageing_based_on": ageing_based_on,
            "range": range,
            "payment_terms_template": payment_terms_template,
            "party_type": party_type,
            "party": party,
            "supplier_group": supplier_group,
            "group_by_party": group_by_party,
            "based_on_payment_terms": based_on_payment_terms,
            "show_remarks": show_remarks,
            "show_future_payments": show_future_payments,
            "in_party_currency": in_party_currency,
            "for_revaluation_journals": for_revaluation_journals,
            "ignore_accounts": ignore_accounts,
            "handle_employee_advances": handle_employee_advances
        },
        ignore_prepared_report=True
    )

    # Custom Columns
    Invoice_details["columns"].insert(3, {'label': 'Enterprise Type', 'fieldname': 'custom_enterprise_type', 'fieldtype': 'Data'})
    Invoice_details["columns"].insert(4, {'label': 'Registration Date', 'fieldname': 'custom_udyam_registration_date', 'fieldtype': 'Data'})
    Invoice_details["columns"].insert(5, {'label': 'Udyam Registration Number', 'fieldname': 'custom_udyam_registration_number', 'fieldtype': 'Data'})
    Invoice_details["columns"].insert(6, {'label': 'Business Category', 'fieldname': 'custom_business_category', 'fieldtype': 'Data'})

    
    if Invoice_details.get("result"):
        Invoice_details["result"].pop()

    # if result is empty
    if not Invoice_details.get("result"):
        return Invoice_details["columns"], []

    # Additional details for suppliers
    # for x in Invoice_details["result"]:
    #     if isinstance(x, dict) and x.get("party_type") == "Supplier":
    #         x["custom_enterprise_type"] = frappe.db.get_value("Supplier", x.get("party"), "custom_enterprise_type") or ""
    #         x["custom_udyam_registration_date"] = frappe.db.get_value("Supplier", x.get("party"), "custom_udyam_registration_date") or ""
    #         x["custom_udyam_registration_number"] = frappe.db.get_value("Supplier", x.get("party"), "custom_udyam_registration_number") or ""
    #         x["custom_business_category"] = frappe.db.get_value("Supplier", x.get("party"), "custom_business_category") or ""

    filtered_result = []

    for x in Invoice_details["result"]:
        if x.get("party_type") == "Supplier":
            # Check if the supplier is MSME registered
            is_msme_registered = frappe.db.get_value("Supplier", x.get("party"), "custom_is_msme_registered")

            if is_msme_registered == 1:
                x["custom_enterprise_type"] = frappe.db.get_value("Supplier", x.get("party"), "custom_enterprise_type") or ""
                x["custom_udyam_registration_date"] = frappe.db.get_value("Supplier", x.get("party"), "custom_udyam_registration_date") or ""
                x["custom_udyam_registration_number"] = frappe.db.get_value("Supplier", x.get("party"), "custom_udyam_registration_number") or ""
                x["custom_business_category"] = frappe.db.get_value("Supplier", x.get("party"), "custom_business_category") or ""
                
                filtered_result.append(x)

    # return columns and data
    return Invoice_details["columns"], filtered_result
