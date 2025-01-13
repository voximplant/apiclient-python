import json
import os
import datetime
import pytz
import requests
import jwt
import time
import sys

class VoximplantException(Exception):
    def __init__(self, msg, code = -1):
        self.message = msg
        self.code = code

    def __str__(self):
        return "{}: {}".format(self.code, self.message)



class VoximplantAPI:
    """Voximplant API access helper"""

    def _api_date_to_py(self, d):
        if d == "":
            return None
        else:
            return datetime.datetime.strptime(d, "%Y-%m-%d").date()

    def _api_datetime_utc_to_py(self, d):
        if d == "":
            return None
        else:
            return datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.utc)

    def _py_datetime_to_api(self, d):
        if d.tzinfo is None:
            return d.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return d.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")

    def build_auth_header(self):
        ts = int(time.time())
        token = jwt.encode({"iss":self.account_id, "iat":ts-5, "exp":ts+24}, self.credentials["private_key"], algorithm='RS256', headers={"kid": self.credentials["key_id"]})
        if isinstance(token, str):
            return 'Bearer '+token
        else:
            return 'Bearer '+token.decode("utf-8")


    def _perform_request(self, cmd, args):
        params = args.copy()
        params["cmd"] = cmd
        headers={'Authorization': self.build_auth_header()}
        result = requests.post("https://{}/platform_api".format(self.endpoint), data=params, headers=headers)
        if result.headers.get("content-type","").split(";")[0].lower() == "application/json":
            return json.loads(result.text)
        else:
            return result.content

    def __init__(self, credentials_file_path = None, endpoint = None):
        if credentials_file_path is None:
            credentials_file_path = os.getenv("VOXIMPLANT_CREDENTIALS")
        with open(credentials_file_path) as credentials_file:
            self.credentials = json.load(credentials_file)
        if self.credentials is None:
            raise VoximplantException("Credentials not found")
        self.account_id = self.credentials["account_id"]
        if not (endpoint is None):
            self.endpoint = endpoint
        else:
            self.endpoint = "api.voximplant.com"

    def _serialize_list(self, p):
        if isinstance(p, str) or (sys.version_info[0] < 3 and isinstance(p, basestring)):
            return p
        try:
            i = iter(p)
            return ";".join([str(i) for i in p])
        except TypeError:
            return str(p)


    def _preprocess_api__error(self, s):
            pass

    def _preprocess_account_info_type(self, s):
        if "created" in s:
            s["created"] = self._api_datetime_utc_to_py(s["created"])
        if "billing_limits" in s:
            self._preprocess_billing_limits_type(s["billing_limits"])

    def _preprocess_billing_limits_type(self, s):
        if "robokassa" in s:
            self._preprocess_billing_limit_info_type(s["robokassa"])
        if "bank_card" in s:
            self._preprocess_bank_card_billing_limit_info_type(s["bank_card"])
        if "invoice" in s:
            self._preprocess_billing_limit_info_type(s["invoice"])

    def _preprocess_billing_limit_info_type(self, s):
            pass

    def _preprocess_bank_card_billing_limit_info_type(self, s):
            pass

    def _preprocess_short_account_info_type(self, s):
            pass

    def _preprocess_cloned_account_type(self, s):
        if "users" in s:
            for k in s["users"]:
                self._preprocess_cloned_user_type(k)
        if "scenarios" in s:
            for k in s["scenarios"]:
                self._preprocess_cloned_scenario_type(k)
        if "applications" in s:
            for k in s["applications"]:
                self._preprocess_cloned_application_type(k)
        if "acd_queues" in s:
            for k in s["acd_queues"]:
                self._preprocess_cloned_acd_queue_type(k)
        if "acd_skills" in s:
            for k in s["acd_skills"]:
                self._preprocess_cloned_acd_skill_type(k)
        if "admin_roles" in s:
            for k in s["admin_roles"]:
                self._preprocess_cloned_admin_role_type(k)
        if "admin_users" in s:
            for k in s["admin_users"]:
                self._preprocess_cloned_admin_user_type(k)

    def _preprocess_account_plan_type(self, s):
        if "next_charge" in s:
            s["next_charge"] = self._api_date_to_py(s["next_charge"])
        if "packages" in s:
            for k in s["packages"]:
                self._preprocess_account_plan_package_type(k)

    def _preprocess_account_plan_package_type(self, s):
            pass

    def _preprocess_plan_type(self, s):
        if "packages" in s:
            for k in s["packages"]:
                self._preprocess_plan_package_type(k)

    def _preprocess_plan_package_type(self, s):
            pass

    def _preprocess_application_info_type(self, s):
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])

    def _preprocess_cloned_application_type(self, s):
        if "users" in s:
            for k in s["users"]:
                self._preprocess_cloned_rule_type(k)

    def _preprocess_user_info_type(self, s):
        if "applications" in s:
            for k in s["applications"]:
                self._preprocess_application_info_type(k)
        if "skills" in s:
            for k in s["skills"]:
                self._preprocess_skill_info_type(k)
        if "acd_queues" in s:
            for k in s["acd_queues"]:
                self._preprocess_acd_queue_operator_info_type(k)
        if "acd_status_change_time" in s:
            s["acd_status_change_time"] = self._api_datetime_utc_to_py(s["acd_status_change_time"])
        if "created" in s:
            s["created"] = self._api_datetime_utc_to_py(s["created"])
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])

    def _preprocess_cloned_user_type(self, s):
            pass

    def _preprocess_scenario_info_type(self, s):
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])

    def _preprocess_cloned_scenario_type(self, s):
            pass

    def _preprocess_rule_info_type(self, s):
        if "scenarios" in s:
            for k in s["scenarios"]:
                self._preprocess_scenario_info_type(k)
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])

    def _preprocess_cloned_rule_type(self, s):
            pass

    def _preprocess_sip_white_list_info_type(self, s):
            pass

    def _preprocess_call_session_info_type(self, s):
        if "start_date" in s:
            s["start_date"] = self._api_datetime_utc_to_py(s["start_date"])
        if "calls" in s:
            for k in s["calls"]:
                self._preprocess_call_info_type(k)
        if "other_resource_usage" in s:
            for k in s["other_resource_usage"]:
                self._preprocess_resource_usage_type(k)
        if "records" in s:
            for k in s["records"]:
                self._preprocess_record_type(k)

    def _preprocess_call_info_type(self, s):
        if "start_time" in s:
            s["start_time"] = self._api_datetime_utc_to_py(s["start_time"])

    def _preprocess_transaction_info_type(self, s):
        if "performed_at" in s:
            s["performed_at"] = self._api_datetime_utc_to_py(s["performed_at"])

    def _preprocess_resource_usage_type(self, s):
        if "used_at" in s:
            s["used_at"] = self._api_datetime_utc_to_py(s["used_at"])

    def _preprocess_record_type(self, s):
        if "start_time" in s:
            s["start_time"] = self._api_datetime_utc_to_py(s["start_time"])

    def _preprocess_audit_log_info_type(self, s):
        if "requested" in s:
            s["requested"] = self._api_datetime_utc_to_py(s["requested"])

    def _preprocess_history_report_type(self, s):
        if "created" in s:
            s["created"] = self._api_datetime_utc_to_py(s["created"])
        if "completed" in s:
            s["completed"] = self._api_datetime_utc_to_py(s["completed"])
        if "last_downloaded" in s:
            s["last_downloaded"] = self._api_datetime_utc_to_py(s["last_downloaded"])
        if "store_until" in s:
            s["store_until"] = self._api_date_to_py(s["store_until"])

    def _preprocess_calculated_call_history_data_type(self, s):
            pass

    def _preprocess_calculated_transaction_history_data_type(self, s):
            pass

    def _preprocess_acd_session_info_type(self, s):
        if "begin_time" in s:
            s["begin_time"] = self._api_datetime_utc_to_py(s["begin_time"])
        if "events" in s:
            for k in s["events"]:
                self._preprocess_acd_session_event_info_type(k)

    def _preprocess_acd_session_event_info_type(self, s):
        if "time" in s:
            s["time"] = self._api_datetime_utc_to_py(s["time"])

    def _preprocess_queue_info_type(self, s):
        if "created" in s:
            s["created"] = self._api_datetime_utc_to_py(s["created"])
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])
        if "deleted" in s:
            s["deleted"] = self._api_datetime_utc_to_py(s["deleted"])
        if "users" in s:
            for k in s["users"]:
                self._preprocess_queue_users(k)
        if "skills" in s:
            for k in s["skills"]:
                self._preprocess_queue_skills(k)

    def _preprocess_queue_skills(self, s):
            pass

    def _preprocess_queue_users(self, s):
            pass

    def _preprocess_acd_state_type(self, s):
        if "acd_queues" in s:
            for k in s["acd_queues"]:
                self._preprocess_acd_queue_state_type(k)

    def _preprocess_acd_operator_aggregation_group_type(self, s):
        if "date" in s:
            s["date"] = self._api_date_to_py(s["date"])
        if "statistics" in s:
            for k in s["statistics"]:
                self._preprocess_acd_operator_statistics_type(k)

    def _preprocess_acd_operator_status_aggregation_group_type(self, s):
        if "date" in s:
            s["date"] = self._api_date_to_py(s["date"])
        if "statistics" in s:
            for k in s["statistics"]:
                self._preprocess_acd_operator_status_statistics_type(k)

    def _preprocess_acd_operator_statistics_type(self, s):
        if "date" in s:
            s["date"] = self._api_date_to_py(s["date"])
        if "SA" in s:
            self._preprocess_acd_statistics_item_type(s["SA"])
        if "TT" in s:
            self._preprocess_acd_statistics_item_type(s["TT"])
        if "ACW" in s:
            self._preprocess_acd_statistics_item_type(s["ACW"])
        if "HT" in s:
            self._preprocess_acd_statistics_item_type(s["HT"])

    def _preprocess_acd_operator_status_statistics_type(self, s):
        if "date" in s:
            s["date"] = self._api_date_to_py(s["date"])
        if "acd_status" in s:
            for k in s["acd_status"]:
                self._preprocess_acd_operator_status_statistics_detail(k)

    def _preprocess_acd_operator_status_statistics_detail(self, s):
        if "OFFLINE" in s:
            self._preprocess_acd_statistics_item_type(s["OFFLINE"])
        if "ONLINE" in s:
            self._preprocess_acd_statistics_item_type(s["ONLINE"])
        if "READY" in s:
            self._preprocess_acd_statistics_item_type(s["READY"])
        if "BANNED" in s:
            self._preprocess_acd_statistics_item_type(s["BANNED"])
        if "IN_SERVICE" in s:
            self._preprocess_acd_statistics_item_type(s["IN_SERVICE"])
        if "AFTER_SERVICE" in s:
            self._preprocess_acd_statistics_item_type(s["AFTER_SERVICE"])
        if "TIMEOUT" in s:
            self._preprocess_acd_statistics_item_type(s["TIMEOUT"])
        if "DND" in s:
            self._preprocess_acd_statistics_item_type(s["DND"])

    def _preprocess_acd_queue_statistics_type(self, s):
        if "date" in s:
            s["date"] = self._api_date_to_py(s["date"])
        if "WT" in s:
            self._preprocess_acd_statistics_item_type(s["WT"])
        if "SA" in s:
            self._preprocess_acd_statistics_item_type(s["SA"])
        if "AT" in s:
            self._preprocess_acd_statistics_item_type(s["AT"])
        if "HT" in s:
            self._preprocess_acd_statistics_item_type(s["HT"])
        if "TT" in s:
            self._preprocess_acd_statistics_item_type(s["TT"])
        if "ACW" in s:
            self._preprocess_acd_statistics_item_type(s["ACW"])
        if "QL" in s:
            self._preprocess_acd_statistics_item_type(s["QL"])
        if "AC" in s:
            for k in s["AC"]:
                self._preprocess_acd_statistics_calls(k)
        if "UAC" in s:
            for k in s["UAC"]:
                self._preprocess_acd_statistics_calls(k)
        if "RC" in s:
            for k in s["RC"]:
                self._preprocess_acd_statistics_calls(k)
        if "SL" in s:
            for k in s["SL"]:
                self._preprocess_acd_queue_statistics_service_level_type(k)

    def _preprocess_acd_queue_statistics_service_level_type(self, s):
            pass

    def _preprocess_acd_statistics_item_type(self, s):
            pass

    def _preprocess_acd_statistics_calls(self, s):
            pass

    def _preprocess_acd_queue_state_type(self, s):
        if "ready_operators" in s:
            for k in s["ready_operators"]:
                self._preprocess_acd_ready_operator_state_type(k)
        if "locked_operators" in s:
            for k in s["locked_operators"]:
                self._preprocess_acd_locked_operator_state_type(k)
        if "after_service_operators" in s:
            for k in s["after_service_operators"]:
                self._preprocess_acd_after_service_operator_state_type(k)
        if "servicing_calls" in s:
            for k in s["servicing_calls"]:
                self._preprocess_acd_servicing_call_state_type(k)
        if "waiting_calls" in s:
            for k in s["waiting_calls"]:
                self._preprocess_acd_waiting_call_state_type(k)

    def _preprocess_acd_ready_operator_state_type(self, s):
            pass

    def _preprocess_acd_locked_operator_state_type(self, s):
        if "unreached" in s:
            s["unreached"] = self._api_datetime_utc_to_py(s["unreached"])
        if "locks" in s:
            for k in s["locks"]:
                self._preprocess_acd_lock(k)
        if "acd_calls" in s:
            for k in s["acd_calls"]:
                self._preprocess_acd_operator_call(k)

    def _preprocess_acd_after_service_operator_state_type(self, s):
            pass

    def _preprocess_acd_lock(self, s):
        if "created" in s:
            s["created"] = self._api_datetime_utc_to_py(s["created"])

    def _preprocess_acd_operator_call(self, s):
        if "begin_time" in s:
            s["begin_time"] = self._api_datetime_utc_to_py(s["begin_time"])
        if "submitted" in s:
            s["submitted"] = self._api_datetime_utc_to_py(s["submitted"])

    def _preprocess_acd_servicing_call_state_type(self, s):
        if "begin_time" in s:
            s["begin_time"] = self._api_datetime_utc_to_py(s["begin_time"])

    def _preprocess_acd_waiting_call_state_type(self, s):
        if "begin_time" in s:
            s["begin_time"] = self._api_datetime_utc_to_py(s["begin_time"])

    def _preprocess_new_phone_info_type(self, s):
            pass

    def _preprocess_attached_phone_info_type(self, s):
        if "phone_next_renewal" in s:
            s["phone_next_renewal"] = self._api_date_to_py(s["phone_next_renewal"])
        if "phone_purchase_date" in s:
            s["phone_purchase_date"] = self._api_datetime_utc_to_py(s["phone_purchase_date"])
        if "unverified_hold_until" in s:
            s["unverified_hold_until"] = self._api_date_to_py(s["unverified_hold_until"])
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])

    def _preprocess_new_attached_phone_info_type(self, s):
        if "unverified_hold_until" in s:
            s["unverified_hold_until"] = self._api_date_to_py(s["unverified_hold_until"])

    def _preprocess_phone_number_country_info_type(self, s):
        if "phone_categories" in s:
            for k in s["phone_categories"]:
                self._preprocess_phone_number_country_category_info_type(k)

    def _preprocess_phone_number_country_category_info_type(self, s):
            pass

    def _preprocess_phone_number_country_state_info_type(self, s):
            pass

    def _preprocess_phone_number_country_region_info_type(self, s):
        if "multiple_numbers_price" in s:
            for k in s["multiple_numbers_price"]:
                self._preprocess_multiple_numbers_price(k)

    def _preprocess_multiple_numbers_price(self, s):
            pass

    def _preprocess_caller_id_info_type(self, s):
        if "verified_until" in s:
            s["verified_until"] = self._api_date_to_py(s["verified_until"])

    def _preprocess_outbound_test_phonenumber_info_type(self, s):
            pass

    def _preprocess_contact_info_type(self, s):
        if "verified" in s:
            s["verified"] = self._api_datetime_utc_to_py(s["verified"])
        if "created" in s:
            s["created"] = self._api_datetime_utc_to_py(s["created"])
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])

    def _preprocess_acd_queue_operator_info_type(self, s):
            pass

    def _preprocess_cloned_acd_queue_type(self, s):
            pass

    def _preprocess_skill_info_type(self, s):
            pass

    def _preprocess_cloned_acd_skill_type(self, s):
            pass

    def _preprocess_exchange_rates(self, s):
            pass

    def _preprocess_resource_price(self, s):
        if "price_groups" in s:
            for k in s["price_groups"]:
                self._preprocess_price_group(k)

    def _preprocess_price_group(self, s):
        if "params" in s:
            self._preprocess_resource_params(s["params"])

    def _preprocess_resource_params(self, s):
            pass

    def _preprocess_call_list_type(self, s):
        if "dt_submit" in s:
            s["dt_submit"] = self._api_datetime_utc_to_py(s["dt_submit"])
        if "dt_complete" in s:
            s["dt_complete"] = self._api_datetime_utc_to_py(s["dt_complete"])

    def _preprocess_call_list_detail_type(self, s):
        if "start_execution_time" in s:
            s["start_execution_time"] = self._api_datetime_utc_to_py(s["start_execution_time"])
        if "finish_execution_time" in s:
            s["finish_execution_time"] = self._api_datetime_utc_to_py(s["finish_execution_time"])

    def _preprocess_sip_registration_type(self, s):
        if "next_subscription_renewal" in s:
            s["next_subscription_renewal"] = self._api_date_to_py(s["next_subscription_renewal"])
        if "purchase_date" in s:
            s["purchase_date"] = self._api_datetime_utc_to_py(s["purchase_date"])

    def _preprocess_admin_role_type(self, s):
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])

    def _preprocess_cloned_admin_role_type(self, s):
            pass

    def _preprocess_admin_user_type(self, s):
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])
        if "admin_roles" in s:
            for k in s["admin_roles"]:
                self._preprocess_admin_role_type(k)

    def _preprocess_cloned_admin_user_type(self, s):
            pass

    def _preprocess_get_money_amount_to_charge_result(self, s):
        if "subscriptions" in s:
            for k in s["subscriptions"]:
                self._preprocess_subscriptions_to_charge_type(k)

    def _preprocess_charge_account_result(self, s):
        if "phones" in s:
            for k in s["phones"]:
                self._preprocess_charged_phone_type(k)

    def _preprocess_charged_phone_type(self, s):
            pass

    def _preprocess_subscriptions_to_charge_type(self, s):
        if "subscription_next_renewal" in s:
            s["subscription_next_renewal"] = self._api_date_to_py(s["subscription_next_renewal"])

    def _preprocess_authorized_account_ip_type(self, s):
        if "created" in s:
            s["created"] = self._api_datetime_utc_to_py(s["created"])

    def _preprocess_contractor_info_type(self, s):
        if "contract" in s:
            self._preprocess_contract_info_type(s["contract"])

    def _preprocess_contract_info_type(self, s):
        if "agreement_date" in s:
            s["agreement_date"] = self._api_date_to_py(s["agreement_date"])

    def _preprocess_contractor_invoice_type(self, s):
        if "invoice_date" in s:
            s["invoice_date"] = self._api_date_to_py(s["invoice_date"])
        if "from_date" in s:
            s["from_date"] = self._api_date_to_py(s["from_date"])
        if "to_date" in s:
            s["to_date"] = self._api_date_to_py(s["to_date"])
        if "services" in s:
            self._preprocess_contractor_invoice_service_type(s["services"])

    def _preprocess_contractor_invoice_service_type(self, s):
            pass

    def _preprocess_account_verification_document(self, s):
        if "uploaded" in s:
            s["uploaded"] = self._api_datetime_utc_to_py(s["uploaded"])

    def _preprocess_account_verification_type(self, s):
        if "unverified_hold_until" in s:
            s["unverified_hold_until"] = self._api_date_to_py(s["unverified_hold_until"])
        if "documents" in s:
            for k in s["documents"]:
                self._preprocess_account_verification_document(k)

    def _preprocess_account_verifications(self, s):
        if "verifications" in s:
            for k in s["verifications"]:
                self._preprocess_account_verification_type(k)

    def _preprocess_subscription_template_type(self, s):
            pass

    def _preprocess_account_callbacks(self, s):
        if "callbacks" in s:
            for k in s["callbacks"]:
                self._preprocess_account_callback(k)

    def _preprocess_account_callback(self, s):
        if "account_document_uploaded" in s:
            self._preprocess_account_document_uploaded_callback(s["account_document_uploaded"])
        if "regulation_address_uploaded" in s:
            self._preprocess_regulation_address_uploaded_callback(s["regulation_address_uploaded"])
        if "account_document_verified" in s:
            self._preprocess_account_document_verified_callback(s["account_document_verified"])
        if "account_is_frozen" in s:
            self._preprocess_account_is_frozen_callback(s["account_is_frozen"])
        if "account_is_unfrozen" in s:
            self._preprocess_account_is_unfrozen_callback(s["account_is_unfrozen"])
        if "activate_successful" in s:
            self._preprocess_activate_successful_callback(s["activate_successful"])
        if "call_history_report" in s:
            self._preprocess_call_history_report_callback(s["call_history_report"])
        if "card_expired" in s:
            self._preprocess_card_expired_callback(s["card_expired"])
        if "card_expires_in_month" in s:
            self._preprocess_card_expires_in_month_callback(s["card_expires_in_month"])
        if "card_payment" in s:
            self._preprocess_card_payment_callback(s["card_payment"])
        if "card_payment_failed" in s:
            self._preprocess_card_payment_failed_callback(s["card_payment_failed"])
        if "robokassa_payment" in s:
            self._preprocess_robokassa_payment_callback(s["robokassa_payment"])
        if "wire_transfer" in s:
            self._preprocess_wire_transfer_callback(s["wire_transfer"])
        if "js_fail" in s:
            self._preprocess_js_fail_callback(s["js_fail"])
        if "min_balance" in s:
            self._preprocess_min_balance_callback(s["min_balance"])
        if "regulation_address_verified" in s:
            self._preprocess_regulation_address_verified_callback(s["regulation_address_verified"])
        if "renewed_subscriptions" in s:
            self._preprocess_renewed_subscriptions_callback(s["renewed_subscriptions"])
        if "reset_account_password_request" in s:
            self._preprocess_reset_account_password_request_callback(s["reset_account_password_request"])
        if "sip_registration_fail" in s:
            self._preprocess_sip_registration_fail_callback(s["sip_registration_fail"])
        if "sip_registration_recovered" in s:
            self._preprocess_sip_registration_recovered_callback(s["sip_registration_recovered"])
        if "stagnant_account" in s:
            self._preprocess_stagnant_account_callback(s["stagnant_account"])
        if "subscription_is_frozen" in s:
            self._preprocess_subscription_is_frozen_callback(s["subscription_is_frozen"])
        if "subscription_is_detached" in s:
            self._preprocess_subscription_is_detached_callback(s["subscription_is_detached"])
        if "transaction_history_report" in s:
            self._preprocess_transaction_history_report_callback(s["transaction_history_report"])
        if "plan_config" in s:
            self._preprocess_plan_config_callback(s["plan_config"])
        if "unverified_subscription_detached" in s:
            self._preprocess_unverified_subscription_detached_callback(s["unverified_subscription_detached"])
        if "expiring_callerid" in s:
            self._preprocess_expiring_caller_id_callback(s["expiring_callerid"])
        if "expired_callerid" in s:
            self._preprocess_expired_caller_id_callback(s["expired_callerid"])
        if "transcription_complete" in s:
            self._preprocess_transcription_complete_callback(s["transcription_complete"])
        if "sms_inbound" in s:
            self._preprocess_inbound_sms_callback(s["sms_inbound"])
        if "new_invoice" in s:
            self._preprocess_new_invoice_callback(s["new_invoice"])
        if "expiring_agreement" in s:
            self._preprocess_expiring_agreement_callback(s["expiring_agreement"])
        if "expired_agreement" in s:
            self._preprocess_expired_agreement_callback(s["expired_agreement"])
        if "restored_agreement_status" in s:
            self._preprocess_restored_agreement_status_callback(s["restored_agreement_status"])
        if "balance_is_changed" in s:
            self._preprocess_balance_is_changed(s["balance_is_changed"])
        if "next_charge_alert" in s:
            self._preprocess_next_charge_alert_callback(s["next_charge_alert"])
        if "certificate_expired" in s:
            self._preprocess_certificate_expired_callback(s["certificate_expired"])
        if "expired_certificates" in s:
            self._preprocess_expired_certificate_callback(s["expired_certificates"])
        if "expiring_certificates" in s:
            self._preprocess_expiring_certificate_callback(s["expiring_certificates"])
        if "account_document_status_updated" in s:
            self._preprocess_account_document_status_updated_callback(s["account_document_status_updated"])
        if "a2p_sms_activated" in s:
            self._preprocess_a2p_activated_callback(s["a2p_sms_activated"])
        if "regulation_address_documents_requested" in s:
            self._preprocess_regulation_address_documents_requested_callback(s["regulation_address_documents_requested"])
        if "invoice_received" in s:
            self._preprocess_invoice_received_callback(s["invoice_received"])

    def _preprocess_a2p_sms_delivery_callback(self, s):
            pass

    def _preprocess_account_document_uploaded_callback(self, s):
        if "uploaded" in s:
            s["uploaded"] = self._api_datetime_utc_to_py(s["uploaded"])

    def _preprocess_balance_is_changed(self, s):
            pass

    def _preprocess_regulation_address_uploaded_callback(self, s):
        if "uploaded" in s:
            s["uploaded"] = self._api_datetime_utc_to_py(s["uploaded"])

    def _preprocess_account_document_verified_callback(self, s):
        if "uploaded" in s:
            s["uploaded"] = self._api_datetime_utc_to_py(s["uploaded"])

    def _preprocess_account_is_frozen_callback(self, s):
            pass

    def _preprocess_account_is_unfrozen_callback(self, s):
            pass

    def _preprocess_activate_successful_callback(self, s):
            pass

    def _preprocess_call_history_report_callback(self, s):
        if "order_date" in s:
            s["order_date"] = self._api_datetime_utc_to_py(s["order_date"])

    def _preprocess_card_expired_callback(self, s):
            pass

    def _preprocess_card_expires_in_month_callback(self, s):
            pass

    def _preprocess_card_payment_callback(self, s):
            pass

    def _preprocess_card_payment_failed_callback(self, s):
            pass

    def _preprocess_robokassa_payment_callback(self, s):
            pass

    def _preprocess_wire_transfer_callback(self, s):
            pass

    def _preprocess_js_fail_callback(self, s):
            pass

    def _preprocess_min_balance_callback(self, s):
            pass

    def _preprocess_regulation_address_verified_callback(self, s):
        if "uploaded" in s:
            s["uploaded"] = self._api_datetime_utc_to_py(s["uploaded"])

    def _preprocess_renewed_subscriptions_callback(self, s):
        if "subscriptions" in s:
            for k in s["subscriptions"]:
                self._preprocess_renewed_subscriptions_callback_item(k)

    def _preprocess_renewed_subscriptions_callback_item(self, s):
        if "next_renewal" in s:
            s["next_renewal"] = self._api_date_to_py(s["next_renewal"])
        if "details" in s:
            for k in s["details"]:
                self._preprocess_subscription_callback_details(k)

    def _preprocess_reset_account_password_request_callback(self, s):
            pass

    def _preprocess_sip_registration_fail_callback(self, s):
        if "sip_registrations" in s:
            for k in s["sip_registrations"]:
                self._preprocess_sip_registration_is_failed_callback_item(k)

    def _preprocess_sip_registration_is_failed_callback_item(self, s):
            pass

    def _preprocess_sip_registration_recovered_callback(self, s):
        if "sip_registrations" in s:
            for k in s["sip_registrations"]:
                self._preprocess_sip_registration_is_recovered_callback_item(k)

    def _preprocess_sip_registration_is_recovered_callback_item(self, s):
            pass

    def _preprocess_subscription_is_detached_callback(self, s):
        if "subscriptions" in s:
            for k in s["subscriptions"]:
                self._preprocess_subscription_is_detached_callback_item(k)

    def _preprocess_subscription_is_detached_callback_item(self, s):
        if "details" in s:
            for k in s["details"]:
                self._preprocess_subscription_callback_details(k)

    def _preprocess_subscription_is_frozen_callback(self, s):
        if "subscriptions" in s:
            for k in s["subscriptions"]:
                self._preprocess_subscription_is_frozen_callback_item(k)

    def _preprocess_subscription_is_frozen_callback_item(self, s):
        if "details" in s:
            for k in s["details"]:
                self._preprocess_subscription_callback_details(k)

    def _preprocess_stagnant_account_callback(self, s):
            pass

    def _preprocess_transaction_history_report_callback(self, s):
        if "order_date" in s:
            s["order_date"] = self._api_datetime_utc_to_py(s["order_date"])

    def _preprocess_plan_config_callback(self, s):
        if "packages" in s:
            for k in s["packages"]:
                self._preprocess_plan_package_config(k)

    def _preprocess_plan_package_config(self, s):
            pass

    def _preprocess_unverified_subscription_detached_callback(self, s):
        if "subscriptions" in s:
            for k in s["subscriptions"]:
                self._preprocess_unverified_subscription_detached_callback_item(k)

    def _preprocess_unverified_subscription_detached_callback_item(self, s):
        if "details" in s:
            for k in s["details"]:
                self._preprocess_subscription_callback_details(k)

    def _preprocess_expiring_caller_id_callback(self, s):
        if "expiration_date" in s:
            s["expiration_date"] = self._api_date_to_py(s["expiration_date"])

    def _preprocess_expired_caller_id_callback(self, s):
            pass

    def _preprocess_transcription_complete_callback(self, s):
        if "transcription_complete" in s:
            self._preprocess_transcription_complete_callback_item(s["transcription_complete"])

    def _preprocess_transcription_complete_callback_item(self, s):
            pass

    def _preprocess_expiring_agreement_callback(self, s):
        if "expiration_date" in s:
            s["expiration_date"] = self._api_date_to_py(s["expiration_date"])

    def _preprocess_next_charge_alert_callback(self, s):
            pass

    def _preprocess_certificate_expired_callback(self, s):
            pass

    def _preprocess_expired_certificate_callback(self, s):
        if "certificates" in s:
            for k in s["certificates"]:
                self._preprocess_certificate_info_type(k)

    def _preprocess_expiring_certificate_callback(self, s):
        if "certificates" in s:
            for k in s["certificates"]:
                self._preprocess_certificate_info_type(k)

    def _preprocess_certificate_info_type(self, s):
        if "expiration_date" in s:
            s["expiration_date"] = self._api_date_to_py(s["expiration_date"])

    def _preprocess_subscription_callback_details(self, s):
        if "phone_numbers" in s:
            for k in s["phone_numbers"]:
                self._preprocess_subscription_callback_details_phone_numbers(k)
        if "sip_registrations" in s:
            for k in s["sip_registrations"]:
                self._preprocess_subscription_callback_details_sip_registrations(k)

    def _preprocess_subscription_callback_details_phone_numbers(self, s):
            pass

    def _preprocess_subscription_callback_details_sip_registrations(self, s):
            pass

    def _preprocess_a2p_activated_callback(self, s):
            pass

    def _preprocess_account_document_status_updated_callback(self, s):
        if "update_time" in s:
            s["update_time"] = self._api_datetime_utc_to_py(s["update_time"])

    def _preprocess_regulation_address_documents_requested_callback(self, s):
        if "update_time" in s:
            s["update_time"] = self._api_datetime_utc_to_py(s["update_time"])

    def _preprocess_invoice_received_callback(self, s):
        if "invoice_date" in s:
            s["invoice_date"] = self._api_datetime_utc_to_py(s["invoice_date"])
        if "receival_date" in s:
            s["receival_date"] = self._api_datetime_utc_to_py(s["receival_date"])

    def _preprocess_zip_code(self, s):
            pass

    def _preprocess_regulation_country(self, s):
            pass

    def _preprocess_regulation_address(self, s):
            pass

    def _preprocess_regulation_region_record(self, s):
            pass

    def _preprocess_bank_card_type(self, s):
        if "last_error" in s:
            self._preprocess_bank_card_error_type(s["last_error"])

    def _preprocess_bank_card_error_type(self, s):
        if "date" in s:
            s["date"] = self._api_datetime_utc_to_py(s["date"])

    def _preprocess_allocate_alfa_bank_payment_result_type(self, s):
            pass

    def _preprocess_pstn_black_list_info_type(self, s):
            pass

    def _preprocess_dialogflow_key_info(self, s):
        if "content" in s:
            self._preprocess_dialogflow_key(s["content"])
        if "applications" in s:
            for k in s["applications"]:
                self._preprocess_application_info_type(k)

    def _preprocess_dialogflow_key(self, s):
            pass

    def _preprocess_push_credential_info(self, s):
        if "content" in s:
            for k in s["content"]:
                self._preprocess_push_credential_content(k)
        if "applications" in s:
            for k in s["applications"]:
                self._preprocess_application_info_type(k)

    def _preprocess_push_credential_content(self, s):
            pass

    def _preprocess_inbound_sms_callback(self, s):
        if "sms_inbound" in s:
            self._preprocess_inbound_sms_callback_item(s["sms_inbound"])

    def _preprocess_inbound_sms_callback_item(self, s):
            pass

    def _preprocess_new_invoice_callback(self, s):
        if "new_invoice" in s:
            self._preprocess_new_invoice_callback_item(s["new_invoice"])

    def _preprocess_new_invoice_callback_item(self, s):
        if "units" in s:
            for k in s["units"]:
                self._preprocess_invoice_units(k)

    def _preprocess_invoice_units(self, s):
            pass

    def _preprocess_record_storage_info_type(self, s):
            pass

    def _preprocess_mgp_info(self, s):
        if "mgp_activated" in s:
            s["mgp_activated"] = self._api_date_to_py(s["mgp_activated"])
        if "mgp_deactivated" in s:
            s["mgp_deactivated"] = self._api_date_to_py(s["mgp_deactivated"])

    def _preprocess_sms_transaction(self, s):
            pass

    def _preprocess_failed_sms(self, s):
            pass

    def _preprocess_mgp_template_info(self, s):
            pass

    def _preprocess_key_info(self, s):
            pass

    def _preprocess_key_view(self, s):
        if "roles" in s:
            for k in s["roles"]:
                self._preprocess_role_view(k)
        if "subuser" in s:
            for k in s["subuser"]:
                self._preprocess_sub_user_view(k)

    def _preprocess_sub_user_view(self, s):
        if "roles" in s:
            for k in s["roles"]:
                self._preprocess_role_view(k)

    def _preprocess_sub_user_id(self, s):
            pass

    def _preprocess_role_view(self, s):
            pass

    def _preprocess_role_group_view(self, s):
            pass

    def _preprocess_child_account_subscription_type(self, s):
        if "next_renewal" in s:
            s["next_renewal"] = self._api_date_to_py(s["next_renewal"])

    def _preprocess_child_account_subscription_template_type(self, s):
            pass

    def _preprocess_sms_history_type(self, s):
        if "processed_date" in s:
            s["processed_date"] = self._api_date_to_py(s["processed_date"])

    def _preprocess_a2p_sms_history_type(self, s):
        if "processing_date" in s:
            s["processing_date"] = self._api_date_to_py(s["processing_date"])

    def _preprocess_expired_agreement_callback(self, s):
            pass

    def _preprocess_restored_agreement_status_callback(self, s):
        if "expiration_date" in s:
            s["expiration_date"] = self._api_date_to_py(s["expiration_date"])

    def _preprocess_get_max_bank_card_payment_result_type(self, s):
            pass

    def _preprocess_get_autocharge_config_result_type(self, s):
            pass

    def _preprocess_get_sq_queues_result(self, s):
        if "created" in s:
            s["created"] = self._api_datetime_utc_to_py(s["created"])
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])

    def _preprocess_get_sq_skills_result(self, s):
        if "created" in s:
            s["created"] = self._api_datetime_utc_to_py(s["created"])
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])

    def _preprocess_get_sq_agents_result(self, s):
        if "sq_statuses" in s:
            for k in s["sq_statuses"]:
                self._preprocess_smart_queue_state__agent__status(k)

    def _preprocess_sq_agent_selection_strategies(self, s):
            pass

    def _preprocess_sq_task_selection_strategies(self, s):
            pass

    def _preprocess_sq_skill_binding_modes(self, s):
            pass

    def _preprocess_sq_agent_binding_modes(self, s):
            pass

    def _preprocess_smart_queue_metrics_result(self, s):
        if "groups" in s:
            for k in s["groups"]:
                self._preprocess_smart_queue_metrics_groups(k)

    def _preprocess_smart_queue_metrics_groups(self, s):
        if "values" in s:
            for k in s["values"]:
                self._preprocess_smart_queue_metrics_groups_values(k)

    def _preprocess_smart_queue_metrics_groups_values(self, s):
        if "from_date" in s:
            s["from_date"] = self._api_datetime_utc_to_py(s["from_date"])
        if "to_date" in s:
            s["to_date"] = self._api_datetime_utc_to_py(s["to_date"])

    def _preprocess_smart_queue_state(self, s):
        if "sq_agents" in s:
            for k in s["sq_agents"]:
                self._preprocess_smart_queue_state__agent(k)
        if "tasks" in s:
            for k in s["tasks"]:
                self._preprocess_smart_queue_state__task(k)

    def _preprocess_smart_queue_state__task(self, s):
        if "sq_skills" in s:
            for k in s["sq_skills"]:
                self._preprocess_smart_queue_task__skill(k)

    def _preprocess_smart_queue_state__agent(self, s):
        if "sq_skills" in s:
            for k in s["sq_skills"]:
                self._preprocess_smart_queue_agent__skill(k)
        if "sq_statuses" in s:
            for k in s["sq_statuses"]:
                self._preprocess_smart_queue_state__agent__status(k)

    def _preprocess_smart_queue_agent__skill(self, s):
            pass

    def _preprocess_smart_queue_task__skill(self, s):
            pass

    def _preprocess_smart_queue_state__agent__status(self, s):
        if "IM" in s:
            self._preprocess_smart_queue_state__agent__status__type(s["IM"])
        if "CALL" in s:
            self._preprocess_smart_queue_state__agent__status__type(s["CALL"])

    def _preprocess_smart_queue_state__agent__status__type(self, s):
        if "from_date" in s:
            s["from_date"] = self._api_datetime_utc_to_py(s["from_date"])

    def _preprocess_key_value_items(self, s):
            pass

    def _preprocess_key_value_pairs(self, s):
            pass

    def _preprocess_key_value_keys(self, s):
            pass

    def _preprocess_account_invoice(self, s):
        if "period" in s:
            self._preprocess_invoice_period(s["period"])
        if "amount" in s:
            self._preprocess_invoice_total_details(s["amount"])
        if "rows" in s:
            self._preprocess_invoice_spending_details(s["rows"])
        if "invoice_date" in s:
            s["invoice_date"] = self._api_date_to_py(s["invoice_date"])

    def _preprocess_invoice_period(self, s):
        if "from" in s:
            s["from"] = self._api_date_to_py(s["from"])
        if "to" in s:
            s["to"] = self._api_date_to_py(s["to"])

    def _preprocess_invoice_total_details(self, s):
            pass

    def _preprocess_invoice_spending_details(self, s):
        if "amount" in s:
            self._preprocess_invoice_total_details(s["amount"])
        if "taxes" in s:
            self._preprocess_invoice_taxes_details(s["taxes"])

    def _preprocess_invoice_taxes_details(self, s):
            pass


    def get_account_info(self, return_live_balance=None):
        """
        Gets the account's info such as account_id, account_name, account_email etc.

        
        :rtype: dict
        """
        params = dict()
        
        
        if return_live_balance is not None:
            params['return_live_balance']=return_live_balance

        
        res = self._perform_request('GetAccountInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_account_info_type(res["result"])
        
        return res

    def set_account_info(self, new_account_email=None, new_account_password=None, language_code=None, location=None, account_first_name=None, account_last_name=None, min_balance_to_notify=None, account_notifications=None, tariff_changing_notifications=None, news_notifications=None, send_js_error=None, billing_address_name=None, billing_address_country_code=None, billing_address_address=None, billing_address_zip=None, billing_address_phone=None, account_custom_data=None, callback_url=None, callback_salt=None, store_outbound_sms=None, store_inbound_sms=None):
        """
        Edits the account's profile.

        
        :rtype: dict
        """
        params = dict()
        
        
        if new_account_email is not None:
            params['new_account_email']=new_account_email

        if new_account_password is not None:
            params['new_account_password']=new_account_password

        if language_code is not None:
            params['language_code']=language_code

        if location is not None:
            params['location']=location

        if account_first_name is not None:
            params['account_first_name']=account_first_name

        if account_last_name is not None:
            params['account_last_name']=account_last_name

        if min_balance_to_notify is not None:
            params['min_balance_to_notify']=min_balance_to_notify

        if account_notifications is not None:
            params['account_notifications']=account_notifications

        if tariff_changing_notifications is not None:
            params['tariff_changing_notifications']=tariff_changing_notifications

        if news_notifications is not None:
            params['news_notifications']=news_notifications

        if send_js_error is not None:
            params['send_js_error']=send_js_error

        if billing_address_name is not None:
            params['billing_address_name']=billing_address_name

        if billing_address_country_code is not None:
            params['billing_address_country_code']=billing_address_country_code

        if billing_address_address is not None:
            params['billing_address_address']=billing_address_address

        if billing_address_zip is not None:
            params['billing_address_zip']=billing_address_zip

        if billing_address_phone is not None:
            params['billing_address_phone']=billing_address_phone

        if account_custom_data is not None:
            params['account_custom_data']=account_custom_data

        if callback_url is not None:
            params['callback_url']=callback_url

        if callback_salt is not None:
            params['callback_salt']=callback_salt

        if store_outbound_sms is not None:
            params['store_outbound_sms']=store_outbound_sms

        if store_inbound_sms is not None:
            params['store_inbound_sms']=store_inbound_sms

        
        res = self._perform_request('SetAccountInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_child_account_info(self, child_account_id=None, child_account_name=None, child_account_email=None, new_child_account_email=None, new_child_account_password=None, account_notifications=None, tariff_changing_notifications=None, news_notifications=None, active=None, language_code=None, location=None, min_balance_to_notify=None, support_robokassa=None, support_bank_card=None, support_invoice=None, can_use_restricted=None):
        """
        Edits the account's profile.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if child_account_id is not None:
            passed_args.append('child_account_id')
        if child_account_name is not None:
            passed_args.append('child_account_name')
        if child_account_email is not None:
            passed_args.append('child_account_email')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_child_account_info")
        if len(passed_args) == 0:
            raise VoximplantException("None of child_account_id, child_account_name, child_account_email passed into set_child_account_info")
        
        
        
        if child_account_id is not None:
            params['child_account_id']=self._serialize_list(child_account_id)

        if child_account_name is not None:
            params['child_account_name']=self._serialize_list(child_account_name)

        if child_account_email is not None:
            params['child_account_email']=self._serialize_list(child_account_email)

        if new_child_account_email is not None:
            params['new_child_account_email']=new_child_account_email

        if new_child_account_password is not None:
            params['new_child_account_password']=new_child_account_password

        if account_notifications is not None:
            params['account_notifications']=account_notifications

        if tariff_changing_notifications is not None:
            params['tariff_changing_notifications']=tariff_changing_notifications

        if news_notifications is not None:
            params['news_notifications']=news_notifications

        if active is not None:
            params['active']=active

        if language_code is not None:
            params['language_code']=language_code

        if location is not None:
            params['location']=location

        if min_balance_to_notify is not None:
            params['min_balance_to_notify']=min_balance_to_notify

        if support_robokassa is not None:
            params['support_robokassa']=support_robokassa

        if support_bank_card is not None:
            params['support_bank_card']=support_bank_card

        if support_invoice is not None:
            params['support_invoice']=support_invoice

        if can_use_restricted is not None:
            params['can_use_restricted']=can_use_restricted

        
        res = self._perform_request('SetChildAccountInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_currency_rate(self, currency, date=None):
        """
        Gets the exchange rate on selected date (per USD).

        
        :rtype: dict
        """
        params = dict()
        
        params['currency']=self._serialize_list(currency)

        
        if date is not None:
            params['date']=date

        
        res = self._perform_request('GetCurrencyRate', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_exchange_rates(res["result"])
        
        return res

    def get_resource_price(self, resource_type=None, price_group_id=None, price_group_name=None, resource_param=None):
        """
        Gets the resource price.

        
        :rtype: dict
        """
        params = dict()
        
        
        if resource_type is not None:
            params['resource_type']=self._serialize_list(resource_type)

        if price_group_id is not None:
            params['price_group_id']=self._serialize_list(price_group_id)

        if price_group_name is not None:
            params['price_group_name']=price_group_name

        if resource_param is not None:
            params['resource_param']=self._serialize_list(resource_param)

        
        res = self._perform_request('GetResourcePrice', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_resource_price(p)
            except TypeError as te:
                pass
        
        return res

    def get_subscription_price(self, subscription_template_id=None, subscription_template_type=None, subscription_template_name=None, count=None, offset=None):
        """
        Gets the subscription template price.

        
        :rtype: dict
        """
        params = dict()
        
        
        if subscription_template_id is not None:
            params['subscription_template_id']=self._serialize_list(subscription_template_id)

        if subscription_template_type is not None:
            params['subscription_template_type']=subscription_template_type

        if subscription_template_name is not None:
            params['subscription_template_name']=subscription_template_name

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetSubscriptionPrice', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_subscription_template_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_children_accounts(self, child_account_id=None, child_account_name=None, child_account_email=None, active=None, frozen=None, ignore_invalid_accounts=None, brief_output=None, medium_output=None, count=None, offset=None, order_by=None, return_live_balance=None):
        """
        Gets the info about all children accounts.

        
        :rtype: dict
        """
        params = dict()
        
        
        if child_account_id is not None:
            params['child_account_id']=self._serialize_list(child_account_id)

        if child_account_name is not None:
            params['child_account_name']=child_account_name

        if child_account_email is not None:
            params['child_account_email']=child_account_email

        if active is not None:
            params['active']=active

        if frozen is not None:
            params['frozen']=frozen

        if ignore_invalid_accounts is not None:
            params['ignore_invalid_accounts']=ignore_invalid_accounts

        if brief_output is not None:
            params['brief_output']=brief_output

        if medium_output is not None:
            params['medium_output']=medium_output

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if order_by is not None:
            params['order_by']=order_by

        if return_live_balance is not None:
            params['return_live_balance']=return_live_balance

        
        res = self._perform_request('GetChildrenAccounts', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_account_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_money_amount_to_charge(self, currency=None, charge_date=None):
        """
        Get the recommended money amount to charge.

        
        :rtype: dict
        """
        params = dict()
        
        
        if currency is not None:
            params['currency']=currency

        if charge_date is not None:
            params['charge_date']=charge_date

        
        res = self._perform_request('GetMoneyAmountToCharge', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_get_money_amount_to_charge_result(res["result"])
        
        return res

    def charge_account(self, phone_id=None, phone_number=None):
        """
        Charges the account in the manual mode. You should call the ChargeAccount function to charge the subscriptions having the auto_charge=false.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if phone_id is not None:
            passed_args.append('phone_id')
        if phone_number is not None:
            passed_args.append('phone_number')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into charge_account")
        if len(passed_args) == 0:
            raise VoximplantException("None of phone_id, phone_number passed into charge_account")
        
        
        
        if phone_id is not None:
            params['phone_id']=self._serialize_list(phone_id)

        if phone_number is not None:
            params['phone_number']=self._serialize_list(phone_number)

        
        res = self._perform_request('ChargeAccount', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_charge_account_result(res["result"])
        
        return res

    def change_account_plan(self, plan_type, plan_subscription_template_id=None):
        """
        Configures the account's plan.<br><br>Please note that when you change the billing plan, we reserve the subscription fee and taxes for the upcoming month. Read more in the <a href='/docs/gettingstarted/billing'>Billing</a> page.

        
        :rtype: dict
        """
        params = dict()
        
        params['plan_type']=plan_type

        
        if plan_subscription_template_id is not None:
            params['plan_subscription_template_id']=plan_subscription_template_id

        
        res = self._perform_request('ChangeAccountPlan', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_account_plans(self, plan_type=None, plan_subscription_template_id=None):
        """
        Gets the account plans with packages.

        
        :rtype: dict
        """
        params = dict()
        
        
        if plan_type is not None:
            params['plan_type']=self._serialize_list(plan_type)

        if plan_subscription_template_id is not None:
            params['plan_subscription_template_id']=self._serialize_list(plan_subscription_template_id)

        
        res = self._perform_request('GetAccountPlans', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_account_plan_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_available_plans(self, plan_type=None, plan_subscription_template_id=None):
        """
        Gets the allowed plans to change.

        
        :rtype: dict
        """
        params = dict()
        
        
        if plan_type is not None:
            params['plan_type']=self._serialize_list(plan_type)

        if plan_subscription_template_id is not None:
            params['plan_subscription_template_id']=self._serialize_list(plan_subscription_template_id)

        
        res = self._perform_request('GetAvailablePlans', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_plan_type(p)
            except TypeError as te:
                pass
        
        return res

    def add_application(self, application_name, secure_record_storage=None):
        """
        Adds a new account's application.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_name']=application_name

        
        if secure_record_storage is not None:
            params['secure_record_storage']=secure_record_storage

        
        res = self._perform_request('AddApplication', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_application(self, application_id=None, application_name=None):
        """
        Deletes the account's application.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_application")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into del_application")
        
        
        
        if application_id is not None:
            params['application_id']=self._serialize_list(application_id)

        if application_name is not None:
            params['application_name']=self._serialize_list(application_name)

        
        res = self._perform_request('DelApplication', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_application_info(self, application_id=None, required_application_name=None, application_name=None, secure_record_storage=None):
        """
        Edits the account's application.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if required_application_name is not None:
            passed_args.append('required_application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_application_info")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, required_application_name passed into set_application_info")
        
        
        
        if application_id is not None:
            params['application_id']=application_id

        if required_application_name is not None:
            params['required_application_name']=required_application_name

        if application_name is not None:
            params['application_name']=application_name

        if secure_record_storage is not None:
            params['secure_record_storage']=secure_record_storage

        
        res = self._perform_request('SetApplicationInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_applications(self, application_id=None, application_name=None, with_rules=None, with_scenarios=None, count=None, offset=None):
        """
        Gets the account's applications.

        
        :rtype: dict
        """
        params = dict()
        
        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if with_rules is not None:
            params['with_rules']=with_rules

        if with_scenarios is not None:
            params['with_scenarios']=with_scenarios

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetApplications', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_application_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def add_user(self, user_name, user_display_name, user_password, application_id=None, application_name=None, parent_accounting=None, user_active=None, user_custom_data=None):
        """
        Adds a new user.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_user")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into add_user")
        
        
        params['user_name']=user_name

        params['user_display_name']=user_display_name

        params['user_password']=user_password

        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if parent_accounting is not None:
            params['parent_accounting']=parent_accounting

        if user_active is not None:
            params['user_active']=user_active

        if user_custom_data is not None:
            params['user_custom_data']=user_custom_data

        
        res = self._perform_request('AddUser', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_user(self, user_id=None, user_name=None, application_id=None, application_name=None):
        """
        Deletes the specified user(s).

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_user")
        if len(passed_args) == 0:
            raise VoximplantException("None of user_id, user_name passed into del_user")
        
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_user")
        
        
        
        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        
        res = self._perform_request('DelUser', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_user_info(self, user_id=None, user_name=None, application_id=None, application_name=None, new_user_name=None, user_display_name=None, user_password=None, parent_accounting=None, user_active=None, user_custom_data=None):
        """
        Edits the user.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_user_info")
        if len(passed_args) == 0:
            raise VoximplantException("None of user_id, user_name passed into set_user_info")
        
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_user_info")
        
        
        
        if user_id is not None:
            params['user_id']=user_id

        if user_name is not None:
            params['user_name']=user_name

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if new_user_name is not None:
            params['new_user_name']=new_user_name

        if user_display_name is not None:
            params['user_display_name']=user_display_name

        if user_password is not None:
            params['user_password']=user_password

        if parent_accounting is not None:
            params['parent_accounting']=parent_accounting

        if user_active is not None:
            params['user_active']=user_active

        if user_custom_data is not None:
            params['user_custom_data']=user_custom_data

        
        res = self._perform_request('SetUserInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_users(self, application_id=None, application_name=None, skill_id=None, excluded_skill_id=None, acd_queue_id=None, excluded_acd_queue_id=None, user_id=None, user_name=None, user_active=None, user_display_name=None, with_skills=None, with_queues=None, acd_status=None, showing_skill_id=None, count=None, offset=None, order_by=None, return_live_balance=None):
        """
        Shows the users of the specified account.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_users")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into get_users")
        
        
        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if skill_id is not None:
            params['skill_id']=skill_id

        if excluded_skill_id is not None:
            params['excluded_skill_id']=excluded_skill_id

        if acd_queue_id is not None:
            params['acd_queue_id']=acd_queue_id

        if excluded_acd_queue_id is not None:
            params['excluded_acd_queue_id']=excluded_acd_queue_id

        if user_id is not None:
            params['user_id']=user_id

        if user_name is not None:
            params['user_name']=user_name

        if user_active is not None:
            params['user_active']=user_active

        if user_display_name is not None:
            params['user_display_name']=user_display_name

        if with_skills is not None:
            params['with_skills']=with_skills

        if with_queues is not None:
            params['with_queues']=with_queues

        if acd_status is not None:
            params['acd_status']=self._serialize_list(acd_status)

        if showing_skill_id is not None:
            params['showing_skill_id']=showing_skill_id

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if order_by is not None:
            params['order_by']=order_by

        if return_live_balance is not None:
            params['return_live_balance']=return_live_balance

        
        res = self._perform_request('GetUsers', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_user_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def transfer_money_to_user(self, amount, user_id=None, user_name=None, application_id=None, application_name=None, currency=None, strict_mode=None, user_transaction_description=None, account_transaction_description=None):
        """
        Transfer the account's money to the user or transfer the user's money to the account if the money amount is negative.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into transfer_money_to_user")
        if len(passed_args) == 0:
            raise VoximplantException("None of user_id, user_name passed into transfer_money_to_user")
        
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into transfer_money_to_user")
        
        
        params['amount']=amount

        
        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if currency is not None:
            params['currency']=currency

        if strict_mode is not None:
            params['strict_mode']=strict_mode

        if user_transaction_description is not None:
            params['user_transaction_description']=user_transaction_description

        if account_transaction_description is not None:
            params['account_transaction_description']=account_transaction_description

        
        res = self._perform_request('TransferMoneyToUser', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def create_call_list(self, rule_id, priority, max_simultaneous, num_attempts, name, file_content, interval_seconds=None, encoding=None, delimiter=None, escape=None, reference_ip=None, server_location=None):
        """
        Adds a new CSV file for call list processing and starts the specified rule immediately. To send a file, use the request body. To set the call time constraints, use the following options in a CSV file: <ul><li>**__start_execution_time** – when the call list processing starts every day, UTC+0 24-h format: HH:mm:ss</li><li>**__end_execution_time** – when the call list processing stops every day,  UTC+0 24-h format: HH:mm:ss</li><li>**__start_at** – when the call list processing starts, UNIX timestamp. If not specified, the processing starts immediately after a method call</li><li>**__task_uuid** – call list UUID. A string up to 40 characters, can contain latin letters, digits, hyphens (-) and colons (:). Unique within the call list</li></ul><br>This method accepts CSV files with custom delimiters, such a commas (,), semicolons (;) and other. To specify a delimiter, pass it to the <b>delimiter</b> parameter.<br/><b>IMPORTANT:</b> the account's balance should be equal or greater than 1 USD. If the balance is lower than 1 USD, the call list processing does not start, or it stops immediately if it is active.

        
        :rtype: dict
        """
        params = dict()
        
        params['rule_id']=rule_id

        params['priority']=priority

        params['max_simultaneous']=max_simultaneous

        params['num_attempts']=num_attempts

        params['name']=name

        params['file_content']=file_content

        
        if interval_seconds is not None:
            params['interval_seconds']=interval_seconds

        if encoding is not None:
            params['encoding']=encoding

        if delimiter is not None:
            params['delimiter']=delimiter

        if escape is not None:
            params['escape']=escape

        if reference_ip is not None:
            params['reference_ip']=reference_ip

        if server_location is not None:
            params['server_location']=server_location

        
        res = self._perform_request('CreateCallList', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_call_lists(self, list_id=None, name=None, is_active=None, from_date=None, to_date=None, type_list=None, count=None, offset=None, application_id=None):
        """
        Get all call lists for the specified user.

        
        :rtype: dict
        """
        params = dict()
        
        
        if list_id is not None:
            params['list_id']=self._serialize_list(list_id)

        if name is not None:
            params['name']=name

        if is_active is not None:
            params['is_active']=is_active

        if from_date is not None:
            params['from_date']=self._py_datetime_to_api(from_date)

        if to_date is not None:
            params['to_date']=self._py_datetime_to_api(to_date)

        if type_list is not None:
            params['type_list']=type_list

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if application_id is not None:
            params['application_id']=self._serialize_list(application_id)

        
        res = self._perform_request('GetCallLists', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_call_list_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_call_list_details(self, list_id, count=None, offset=None, output=None, encoding=None, delimiter=None):
        """
        Gets details of the specified call list. Returns a CSV file by default.

        
        :rtype: dict
        """
        params = dict()
        
        params['list_id']=list_id

        
        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if output is not None:
            params['output']=output

        if encoding is not None:
            params['encoding']=encoding

        if delimiter is not None:
            params['delimiter']=delimiter

        
        res = self._perform_request('GetCallListDetails', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_call_list_detail_type(p)
            except TypeError as te:
                pass
        
        return res

    def edit_call_list_task(self, list_id, task_id=None, task_uuid=None, start_at=None, attempts_left=None, custom_data=None, min_execution_time=None):
        """
        Edits the specified call list's task.

        
        :rtype: dict
        """
        params = dict()
        
        params['list_id']=list_id

        
        if task_id is not None:
            params['task_id']=task_id

        if task_uuid is not None:
            params['task_uuid']=task_uuid

        if start_at is not None:
            params['start_at']=self._py_datetime_to_api(start_at)

        if attempts_left is not None:
            params['attempts_left']=attempts_left

        if custom_data is not None:
            params['custom_data']=custom_data

        if min_execution_time is not None:
            params['min_execution_time']=self._py_datetime_to_api(min_execution_time)

        
        res = self._perform_request('EditCallListTask', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def stop_call_list_processing(self, list_id):
        """
        Stops processing the specified call list.

        
        :rtype: dict
        """
        params = dict()
        
        params['list_id']=list_id

        
        
        res = self._perform_request('StopCallListProcessing', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def recover_call_list(self, list_id):
        """
        Resume processing the specified call list.

        
        :rtype: dict
        """
        params = dict()
        
        params['list_id']=list_id

        
        
        res = self._perform_request('RecoverCallList', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def add_scenario(self, scenario_name, scenario_script=None, rule_id=None, rule_name=None, rewrite=None, application_id=None, application_name=None):
        """
        Adds a new scenario to the <a href="https://voximplant.com/docs/gettingstarted/basicconcepts/scenarios#shared-scenarios">Shared</a> folder, so the scenario is available in all the existing applications. Please use the POST method.

        
        :rtype: dict
        """
        params = dict()
        
        params['scenario_name']=scenario_name

        
        if scenario_script is not None:
            params['scenario_script']=scenario_script

        if rule_id is not None:
            params['rule_id']=rule_id

        if rule_name is not None:
            params['rule_name']=rule_name

        if rewrite is not None:
            params['rewrite']=rewrite

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        
        res = self._perform_request('AddScenario', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_scenario(self, scenario_id=None, scenario_name=None):
        """
        Deletes the scenario.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if scenario_id is not None:
            passed_args.append('scenario_id')
        if scenario_name is not None:
            passed_args.append('scenario_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_scenario")
        if len(passed_args) == 0:
            raise VoximplantException("None of scenario_id, scenario_name passed into del_scenario")
        
        
        
        if scenario_id is not None:
            params['scenario_id']=self._serialize_list(scenario_id)

        if scenario_name is not None:
            params['scenario_name']=self._serialize_list(scenario_name)

        
        res = self._perform_request('DelScenario', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def bind_scenario(self, scenario_id=None, scenario_name=None, rule_id=None, rule_name=None, application_id=None, application_name=None, bind=None):
        """
        Bind the scenario list to the rule. You should specify the application_id or application_name if you specify the rule_name. Please note, the scenario and the routing rule need to be within the same application.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if scenario_id is not None:
            passed_args.append('scenario_id')
        if scenario_name is not None:
            passed_args.append('scenario_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_scenario")
        if len(passed_args) == 0:
            raise VoximplantException("None of scenario_id, scenario_name passed into bind_scenario")
        
        
        passed_args = []
        if rule_id is not None:
            passed_args.append('rule_id')
        if rule_name is not None:
            passed_args.append('rule_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_scenario")
        if len(passed_args) == 0:
            raise VoximplantException("None of rule_id, rule_name passed into bind_scenario")
        
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_scenario")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into bind_scenario")
        
        
        
        if scenario_id is not None:
            params['scenario_id']=self._serialize_list(scenario_id)

        if scenario_name is not None:
            params['scenario_name']=self._serialize_list(scenario_name)

        if rule_id is not None:
            params['rule_id']=rule_id

        if rule_name is not None:
            params['rule_name']=rule_name

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if bind is not None:
            params['bind']=bind

        
        res = self._perform_request('BindScenario', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_scenarios(self, scenario_id=None, scenario_name=None, with_script=None, count=None, offset=None, application_id=None, application_name=None):
        """
        Gets the account's scenarios.

        
        :rtype: dict
        """
        params = dict()
        
        
        if scenario_id is not None:
            params['scenario_id']=scenario_id

        if scenario_name is not None:
            params['scenario_name']=scenario_name

        if with_script is not None:
            params['with_script']=with_script

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        
        res = self._perform_request('GetScenarios', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_scenario_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def set_scenario_info(self, scenario_id=None, required_scenario_name=None, scenario_name=None, scenario_script=None):
        """
        Edits the scenario. You can edit the scenario's name and body. Please use the POST method.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if scenario_id is not None:
            passed_args.append('scenario_id')
        if required_scenario_name is not None:
            passed_args.append('required_scenario_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_scenario_info")
        if len(passed_args) == 0:
            raise VoximplantException("None of scenario_id, required_scenario_name passed into set_scenario_info")
        
        
        
        if scenario_id is not None:
            params['scenario_id']=scenario_id

        if required_scenario_name is not None:
            params['required_scenario_name']=required_scenario_name

        if scenario_name is not None:
            params['scenario_name']=scenario_name

        if scenario_script is not None:
            params['scenario_script']=scenario_script

        
        res = self._perform_request('SetScenarioInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def reorder_scenarios(self, rule_id=None, rule_name=None, scenario_id=None):
        """
        Configures the order of scenarios that are assigned to the specified rule.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if rule_id is not None:
            passed_args.append('rule_id')
        if rule_name is not None:
            passed_args.append('rule_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into reorder_scenarios")
        if len(passed_args) == 0:
            raise VoximplantException("None of rule_id, rule_name passed into reorder_scenarios")
        
        
        
        if rule_id is not None:
            params['rule_id']=rule_id

        if rule_name is not None:
            params['rule_name']=rule_name

        if scenario_id is not None:
            params['scenario_id']=self._serialize_list(scenario_id)

        
        res = self._perform_request('ReorderScenarios', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def start_scenarios(self, rule_id, user_id=None, user_name=None, application_id=None, application_name=None, script_custom_data=None, reference_ip=None, server_location=None):
        """
        Runs JavaScript scenarios on a Voximplant server. The scenarios run in a new media session. To start a scenario, pass the routing rule ID associated with the necessary scenario. You can use both GET and POST requests, but we recommend using the POST mode if you pass some data in the custom_data field. The maximum number of simultaneous requests is 200. If you exceed this number, you get the 429 error code.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into start_scenarios")
        
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into start_scenarios")
        
        
        params['rule_id']=rule_id

        
        if user_id is not None:
            params['user_id']=user_id

        if user_name is not None:
            params['user_name']=user_name

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if script_custom_data is not None:
            params['script_custom_data']=script_custom_data

        if reference_ip is not None:
            params['reference_ip']=reference_ip

        if server_location is not None:
            params['server_location']=server_location

        
        res = self._perform_request('StartScenarios', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def start_conference(self, conference_name, rule_id, user_id=None, user_name=None, application_id=None, application_name=None, script_custom_data=None, reference_ip=None, server_location=None):
        """
        Runs a session for video conferencing or joins the existing video conference session.<br/><br/>When you create a session by calling this method, a scenario runs on one of the servers dedicated to video conferencing. All further method calls with the same **conference_name** do not create a new video conference session but join the existing one.<br/><br/>Use the [StartScenarios] method for creating audio conferences.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into start_conference")
        
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into start_conference")
        
        
        params['conference_name']=conference_name

        params['rule_id']=rule_id

        
        if user_id is not None:
            params['user_id']=user_id

        if user_name is not None:
            params['user_name']=user_name

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if script_custom_data is not None:
            params['script_custom_data']=script_custom_data

        if reference_ip is not None:
            params['reference_ip']=reference_ip

        if server_location is not None:
            params['server_location']=server_location

        
        res = self._perform_request('StartConference', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def add_rule(self, rule_name, rule_pattern, application_id=None, application_name=None, rule_pattern_exclude=None, video_conference=None, bind_key_id=None, scenario_id=None, scenario_name=None):
        """
        Adds a new rule for the application.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_rule")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into add_rule")
        
        
        passed_args = []
        if scenario_id is not None:
            passed_args.append('scenario_id')
        if scenario_name is not None:
            passed_args.append('scenario_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_rule")
        if len(passed_args) == 0:
            raise VoximplantException("None of scenario_id, scenario_name passed into add_rule")
        
        
        params['rule_name']=rule_name

        params['rule_pattern']=rule_pattern

        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if rule_pattern_exclude is not None:
            params['rule_pattern_exclude']=rule_pattern_exclude

        if video_conference is not None:
            params['video_conference']=video_conference

        if bind_key_id is not None:
            params['bind_key_id']=bind_key_id

        if scenario_id is not None:
            params['scenario_id']=self._serialize_list(scenario_id)

        if scenario_name is not None:
            params['scenario_name']=self._serialize_list(scenario_name)

        
        res = self._perform_request('AddRule', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_rule(self, rule_id=None, rule_name=None, application_id=None, application_name=None):
        """
        Deletes the rule.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if rule_id is not None:
            passed_args.append('rule_id')
        if rule_name is not None:
            passed_args.append('rule_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_rule")
        if len(passed_args) == 0:
            raise VoximplantException("None of rule_id, rule_name passed into del_rule")
        
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_rule")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into del_rule")
        
        
        
        if rule_id is not None:
            params['rule_id']=self._serialize_list(rule_id)

        if rule_name is not None:
            params['rule_name']=self._serialize_list(rule_name)

        if application_id is not None:
            params['application_id']=self._serialize_list(application_id)

        if application_name is not None:
            params['application_name']=self._serialize_list(application_name)

        
        res = self._perform_request('DelRule', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_rule_info(self, rule_id, rule_name=None, rule_pattern=None, rule_pattern_exclude=None, video_conference=None, bind_key_id=None):
        """
        Edits the rule.

        
        :rtype: dict
        """
        params = dict()
        
        params['rule_id']=rule_id

        
        if rule_name is not None:
            params['rule_name']=rule_name

        if rule_pattern is not None:
            params['rule_pattern']=rule_pattern

        if rule_pattern_exclude is not None:
            params['rule_pattern_exclude']=rule_pattern_exclude

        if video_conference is not None:
            params['video_conference']=video_conference

        if bind_key_id is not None:
            params['bind_key_id']=bind_key_id

        
        res = self._perform_request('SetRuleInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_rules(self, application_id=None, application_name=None, rule_id=None, rule_name=None, video_conference=None, attached_key_id=None, template=None, with_scenarios=None, count=None, offset=None):
        """
        Gets the rules.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_rules")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into get_rules")
        
        
        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if rule_id is not None:
            params['rule_id']=rule_id

        if rule_name is not None:
            params['rule_name']=rule_name

        if video_conference is not None:
            params['video_conference']=video_conference

        if attached_key_id is not None:
            params['attached_key_id']=attached_key_id

        if template is not None:
            params['template']=template

        if with_scenarios is not None:
            params['with_scenarios']=with_scenarios

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetRules', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_rule_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def reorder_rules(self, rule_id):
        """
        Configures the rules' order in the <a href='//manage.voximplant.com/applications'>Applications</a> section of Control panel. Note: the rules must belong to the same application!

        
        :rtype: dict
        """
        params = dict()
        
        params['rule_id']=self._serialize_list(rule_id)

        
        
        res = self._perform_request('ReorderRules', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_call_history(self, from_date, to_date, call_session_history_id=None, application_id=None, application_name=None, user_id=None, rule_name=None, remote_number=None, local_number=None, call_session_history_custom_data=None, with_calls=None, with_records=None, with_other_resources=None, child_account_id=None, children_calls_only=None, with_header=None, desc_order=None, with_total_count=None, count=None, offset=None, output=None, is_async=None):
        """
        Gets the account's call history, including call duration, cost, logs and other call information. You can filter the call history by a certain date

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_call_history")
        
        
        params['from_date']=self._py_datetime_to_api(from_date)

        params['to_date']=self._py_datetime_to_api(to_date)

        
        if call_session_history_id is not None:
            params['call_session_history_id']=self._serialize_list(call_session_history_id)

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if rule_name is not None:
            params['rule_name']=rule_name

        if remote_number is not None:
            params['remote_number']=self._serialize_list(remote_number)

        if local_number is not None:
            params['local_number']=self._serialize_list(local_number)

        if call_session_history_custom_data is not None:
            params['call_session_history_custom_data']=call_session_history_custom_data

        if with_calls is not None:
            params['with_calls']=with_calls

        if with_records is not None:
            params['with_records']=with_records

        if with_other_resources is not None:
            params['with_other_resources']=with_other_resources

        if child_account_id is not None:
            params['child_account_id']=self._serialize_list(child_account_id)

        if children_calls_only is not None:
            params['children_calls_only']=children_calls_only

        if with_header is not None:
            params['with_header']=with_header

        if desc_order is not None:
            params['desc_order']=desc_order

        if with_total_count is not None:
            params['with_total_count']=with_total_count

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if output is not None:
            params['output']=output

        if is_async is not None:
            params['is_async']=is_async

        
        res = self._perform_request('GetCallHistory', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_call_session_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_brief_call_history(self, from_date, to_date, output, is_async, call_session_history_id=None, application_id=None, application_name=None, rule_name=None, remote_number=None, local_number=None, call_session_history_custom_data=None, with_header=None, desc_order=None):
        """
        Gets the account's brief call history. Use the [GetHistoryReports], [DownloadHistoryReport] methods to download the report.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_brief_call_history")
        
        
        params['from_date']=self._py_datetime_to_api(from_date)

        params['to_date']=self._py_datetime_to_api(to_date)

        params['output']=output

        params['is_async']=is_async

        
        if call_session_history_id is not None:
            params['call_session_history_id']=self._serialize_list(call_session_history_id)

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if rule_name is not None:
            params['rule_name']=rule_name

        if remote_number is not None:
            params['remote_number']=self._serialize_list(remote_number)

        if local_number is not None:
            params['local_number']=self._serialize_list(local_number)

        if call_session_history_custom_data is not None:
            params['call_session_history_custom_data']=call_session_history_custom_data

        if with_header is not None:
            params['with_header']=with_header

        if desc_order is not None:
            params['desc_order']=desc_order

        
        res = self._perform_request('GetBriefCallHistory', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_history_reports(self, history_report_id=None, history_type=None, created_from=None, created_to=None, is_completed=None, desc_order=None, count=None, offset=None, application_id=None):
        """
        Gets the list of history reports and their statuses. The method returns info about reports made via [GetCallHistory] with the specified __output=csv__ and **is_async=true** parameters. Note that the **file_size** field in response is valid only for video calls.

        
        :rtype: dict
        """
        params = dict()
        
        
        if history_report_id is not None:
            params['history_report_id']=history_report_id

        if history_type is not None:
            params['history_type']=self._serialize_list(history_type)

        if created_from is not None:
            params['created_from']=self._py_datetime_to_api(created_from)

        if created_to is not None:
            params['created_to']=self._py_datetime_to_api(created_to)

        if is_completed is not None:
            params['is_completed']=is_completed

        if desc_order is not None:
            params['desc_order']=desc_order

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if application_id is not None:
            params['application_id']=self._serialize_list(application_id)

        
        res = self._perform_request('GetHistoryReports', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_history_report_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_transaction_history(self, from_date, to_date, transaction_id=None, transaction_type=None, user_id=None, child_account_id=None, children_transactions_only=None, users_transactions_only=None, desc_order=None, count=None, offset=None, output=None, is_async=None, is_uncommitted=None):
        """
        Gets the transaction history.

        
        :rtype: dict
        """
        params = dict()
        
        params['from_date']=self._py_datetime_to_api(from_date)

        params['to_date']=self._py_datetime_to_api(to_date)

        
        if transaction_id is not None:
            params['transaction_id']=self._serialize_list(transaction_id)

        if transaction_type is not None:
            params['transaction_type']=self._serialize_list(transaction_type)

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if child_account_id is not None:
            params['child_account_id']=self._serialize_list(child_account_id)

        if children_transactions_only is not None:
            params['children_transactions_only']=children_transactions_only

        if users_transactions_only is not None:
            params['users_transactions_only']=users_transactions_only

        if desc_order is not None:
            params['desc_order']=desc_order

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if output is not None:
            params['output']=output

        if is_async is not None:
            params['is_async']=is_async

        if is_uncommitted is not None:
            params['is_uncommitted']=is_uncommitted

        
        res = self._perform_request('GetTransactionHistory', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_transaction_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def delete_record(self, record_url=None, record_id=None):
        """
        Try to remove a record and transcription files.

        
        :rtype: dict
        """
        params = dict()
        
        
        if record_url is not None:
            params['record_url']=record_url

        if record_id is not None:
            params['record_id']=record_id

        
        res = self._perform_request('DeleteRecord', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_acd_history(self, from_date, to_date, acd_session_history_id=None, acd_request_id=None, acd_queue_id=None, user_id=None, operator_hangup=None, unserviced=None, min_waiting_time=None, rejected=None, with_events=None, with_header=None, desc_order=None, count=None, offset=None, output=None):
        """
        Gets the ACD history.

        
        :rtype: dict
        """
        params = dict()
        
        params['from_date']=self._py_datetime_to_api(from_date)

        params['to_date']=self._py_datetime_to_api(to_date)

        
        if acd_session_history_id is not None:
            params['acd_session_history_id']=self._serialize_list(acd_session_history_id)

        if acd_request_id is not None:
            params['acd_request_id']=self._serialize_list(acd_request_id)

        if acd_queue_id is not None:
            params['acd_queue_id']=self._serialize_list(acd_queue_id)

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if operator_hangup is not None:
            params['operator_hangup']=operator_hangup

        if unserviced is not None:
            params['unserviced']=unserviced

        if min_waiting_time is not None:
            params['min_waiting_time']=min_waiting_time

        if rejected is not None:
            params['rejected']=rejected

        if with_events is not None:
            params['with_events']=with_events

        if with_header is not None:
            params['with_header']=with_header

        if desc_order is not None:
            params['desc_order']=desc_order

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if output is not None:
            params['output']=output

        
        res = self._perform_request('GetACDHistory', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_acd_session_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_audit_log(self, from_date, to_date, audit_log_id=None, filtered_admin_user_id=None, filtered_ip=None, filtered_cmd=None, advanced_filters=None, with_header=None, desc_order=None, with_total_count=None, count=None, offset=None, output=None, is_async=None):
        """
        Gets the history of account changes.

        
        :rtype: dict
        """
        params = dict()
        
        params['from_date']=self._py_datetime_to_api(from_date)

        params['to_date']=self._py_datetime_to_api(to_date)

        
        if audit_log_id is not None:
            params['audit_log_id']=self._serialize_list(audit_log_id)

        if filtered_admin_user_id is not None:
            params['filtered_admin_user_id']=filtered_admin_user_id

        if filtered_ip is not None:
            params['filtered_ip']=self._serialize_list(filtered_ip)

        if filtered_cmd is not None:
            params['filtered_cmd']=self._serialize_list(filtered_cmd)

        if advanced_filters is not None:
            params['advanced_filters']=advanced_filters

        if with_header is not None:
            params['with_header']=with_header

        if desc_order is not None:
            params['desc_order']=desc_order

        if with_total_count is not None:
            params['with_total_count']=with_total_count

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if output is not None:
            params['output']=output

        if is_async is not None:
            params['is_async']=is_async

        
        res = self._perform_request('GetAuditLog', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_audit_log_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def add_pstn_black_list_item(self, pstn_blacklist_phone):
        """
        Add a new phone number to the PSTN blacklist. Use blacklist to block incoming calls from specified phone numbers to numbers purchased from Voximplant. Since we have no control over exact phone number format for calls from SIP integrations, blacklisting such numbers should be done via JavaScript scenarios.

        
        :rtype: dict
        """
        params = dict()
        
        params['pstn_blacklist_phone']=pstn_blacklist_phone

        
        
        res = self._perform_request('AddPstnBlackListItem', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_pstn_black_list_item(self, pstn_blacklist_id, pstn_blacklist_phone):
        """
        Update the PSTN blacklist item. BlackList works for numbers that are purchased from Voximplant only. Since we have no control over exact phone number format for calls from SIP integrations, blacklisting such numbers should be done via JavaScript scenarios.

        
        :rtype: dict
        """
        params = dict()
        
        params['pstn_blacklist_id']=pstn_blacklist_id

        params['pstn_blacklist_phone']=pstn_blacklist_phone

        
        
        res = self._perform_request('SetPstnBlackListItem', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_pstn_black_list_item(self, pstn_blacklist_id):
        """
        Remove phone number from the PSTN blacklist.

        
        :rtype: dict
        """
        params = dict()
        
        params['pstn_blacklist_id']=pstn_blacklist_id

        
        
        res = self._perform_request('DelPstnBlackListItem', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_pstn_black_list(self, pstn_blacklist_id=None, pstn_blacklist_phone=None, count=None, offset=None):
        """
        Get the whole PSTN blacklist.

        
        :rtype: dict
        """
        params = dict()
        
        
        if pstn_blacklist_id is not None:
            params['pstn_blacklist_id']=pstn_blacklist_id

        if pstn_blacklist_phone is not None:
            params['pstn_blacklist_phone']=pstn_blacklist_phone

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetPstnBlackList', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_pstn_black_list_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def add_sip_white_list_item(self, sip_whitelist_network, description=None):
        """
        Adds a new network address to the SIP white list.

        
        :rtype: dict
        """
        params = dict()
        
        params['sip_whitelist_network']=sip_whitelist_network

        
        if description is not None:
            params['description']=description

        
        res = self._perform_request('AddSipWhiteListItem', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_sip_white_list_item(self, sip_whitelist_id):
        """
        Deletes the network address from the SIP white list.

        
        :rtype: dict
        """
        params = dict()
        
        params['sip_whitelist_id']=sip_whitelist_id

        
        
        res = self._perform_request('DelSipWhiteListItem', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_sip_white_list_item(self, sip_whitelist_id, sip_whitelist_network, description=None):
        """
        Edits the SIP white list.

        
        :rtype: dict
        """
        params = dict()
        
        params['sip_whitelist_id']=sip_whitelist_id

        params['sip_whitelist_network']=sip_whitelist_network

        
        if description is not None:
            params['description']=description

        
        res = self._perform_request('SetSipWhiteListItem', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_sip_white_list(self, sip_whitelist_id=None, count=None, offset=None):
        """
        Gets the SIP white list.

        
        :rtype: dict
        """
        params = dict()
        
        
        if sip_whitelist_id is not None:
            params['sip_whitelist_id']=sip_whitelist_id

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetSipWhiteList', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_sip_white_list_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def create_sip_registration(self, sip_username, proxy, auth_user=None, outbound_proxy=None, password=None, is_persistent=None, application_id=None, application_name=None, rule_id=None, rule_name=None, user_id=None, user_name=None):
        """
        Create a new SIP registration. You should specify the application_id or application_name if you specify the rule_name or user_id, or user_name. You should set is_persistent=true if you specify the user_id or user_name. You can bind only one SIP registration to the user (the previous SIP registration are automatically unbound).<br><br>Please note that when you create a SIP registration, we reserve the subscription fee and taxes for the upcoming month. Read more in the <a href='/docs/gettingstarted/billing'>Billing</a> page.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into create_sip_registration")
        
        
        passed_args = []
        if rule_id is not None:
            passed_args.append('rule_id')
        if rule_name is not None:
            passed_args.append('rule_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into create_sip_registration")
        
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into create_sip_registration")
        
        
        params['sip_username']=sip_username

        params['proxy']=proxy

        
        if auth_user is not None:
            params['auth_user']=auth_user

        if outbound_proxy is not None:
            params['outbound_proxy']=outbound_proxy

        if password is not None:
            params['password']=password

        if is_persistent is not None:
            params['is_persistent']=is_persistent

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if rule_id is not None:
            params['rule_id']=rule_id

        if rule_name is not None:
            params['rule_name']=rule_name

        if user_id is not None:
            params['user_id']=user_id

        if user_name is not None:
            params['user_name']=user_name

        
        res = self._perform_request('CreateSipRegistration', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def update_sip_registration(self, sip_registration_id, sip_username=None, proxy=None, auth_user=None, outbound_proxy=None, password=None, application_id=None, application_name=None, rule_id=None, rule_name=None, user_id=None, user_name=None):
        """
        Update SIP registration. You should specify the application_id or application_name if you specify the rule_name or user_id, or user_name. You can bind only one SIP registration to the user (the previous SIP registration is automatically unbound).

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into update_sip_registration")
        
        
        passed_args = []
        if rule_id is not None:
            passed_args.append('rule_id')
        if rule_name is not None:
            passed_args.append('rule_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into update_sip_registration")
        
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into update_sip_registration")
        
        
        params['sip_registration_id']=sip_registration_id

        
        if sip_username is not None:
            params['sip_username']=sip_username

        if proxy is not None:
            params['proxy']=proxy

        if auth_user is not None:
            params['auth_user']=auth_user

        if outbound_proxy is not None:
            params['outbound_proxy']=outbound_proxy

        if password is not None:
            params['password']=password

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if rule_id is not None:
            params['rule_id']=rule_id

        if rule_name is not None:
            params['rule_name']=rule_name

        if user_id is not None:
            params['user_id']=user_id

        if user_name is not None:
            params['user_name']=user_name

        
        res = self._perform_request('UpdateSipRegistration', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def bind_sip_registration(self, sip_registration_id=None, application_id=None, application_name=None, rule_id=None, rule_name=None, user_id=None, user_name=None, bind=None):
        """
        Bind the SIP registration to the application/user or unbind the SIP registration from the application/user. You should specify the application_id or application_name if you specify the rule_name or user_id, or user_name. You should specify the sip_registration_id if you set bind=true. You can bind only one SIP registration to the user (the previous SIP registration is automatically unbound).

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_sip_registration")
        
        
        passed_args = []
        if rule_id is not None:
            passed_args.append('rule_id')
        if rule_name is not None:
            passed_args.append('rule_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_sip_registration")
        
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_sip_registration")
        
        
        
        if sip_registration_id is not None:
            params['sip_registration_id']=sip_registration_id

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if rule_id is not None:
            params['rule_id']=rule_id

        if rule_name is not None:
            params['rule_name']=rule_name

        if user_id is not None:
            params['user_id']=user_id

        if user_name is not None:
            params['user_name']=user_name

        if bind is not None:
            params['bind']=bind

        
        res = self._perform_request('BindSipRegistration', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def delete_sip_registration(self, sip_registration_id):
        """
        Delete SIP registration.

        
        :rtype: dict
        """
        params = dict()
        
        params['sip_registration_id']=sip_registration_id

        
        
        res = self._perform_request('DeleteSipRegistration', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_sip_registrations(self, sip_registration_id=None, sip_username=None, deactivated=None, successful=None, is_persistent=None, application_id=None, application_name=None, is_bound_to_application=None, rule_id=None, rule_name=None, user_id=None, user_name=None, proxy=None, in_progress=None, status_code=None, count=None, offset=None):
        """
        Get active SIP registrations.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_sip_registrations")
        
        
        passed_args = []
        if rule_id is not None:
            passed_args.append('rule_id')
        if rule_name is not None:
            passed_args.append('rule_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_sip_registrations")
        if len(passed_args) == 0:
            raise VoximplantException("None of rule_id, rule_name passed into get_sip_registrations")
        
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_sip_registrations")
        if len(passed_args) == 0:
            raise VoximplantException("None of user_id, user_name passed into get_sip_registrations")
        
        
        
        if sip_registration_id is not None:
            params['sip_registration_id']=sip_registration_id

        if sip_username is not None:
            params['sip_username']=sip_username

        if deactivated is not None:
            params['deactivated']=deactivated

        if successful is not None:
            params['successful']=successful

        if is_persistent is not None:
            params['is_persistent']=is_persistent

        if application_id is not None:
            params['application_id']=self._serialize_list(application_id)

        if application_name is not None:
            params['application_name']=self._serialize_list(application_name)

        if is_bound_to_application is not None:
            params['is_bound_to_application']=is_bound_to_application

        if rule_id is not None:
            params['rule_id']=self._serialize_list(rule_id)

        if rule_name is not None:
            params['rule_name']=self._serialize_list(rule_name)

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if proxy is not None:
            params['proxy']=self._serialize_list(proxy)

        if in_progress is not None:
            params['in_progress']=in_progress

        if status_code is not None:
            params['status_code']=status_code

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetSipRegistrations', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_sip_registration_type(p)
            except TypeError as te:
                pass
        
        return res

    def attach_phone_number(self, country_code, phone_category_name, phone_region_id, phone_count=None, phone_number=None, country_state=None, regulation_address_id=None):
        """
        Attach the phone number to the account. Note that phone numbers of some countries may require additional verification steps.<br><br>Please note that when you purchase a phone number, we reserve the subscription fee and taxes for the upcoming month. Read more in the <a href='/docs/gettingstarted/billing'>Billing</a> page.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if phone_count is not None:
            passed_args.append('phone_count')
        if phone_number is not None:
            passed_args.append('phone_number')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into attach_phone_number")
        if len(passed_args) == 0:
            raise VoximplantException("None of phone_count, phone_number passed into attach_phone_number")
        
        
        params['country_code']=country_code

        params['phone_category_name']=phone_category_name

        params['phone_region_id']=phone_region_id

        
        if phone_count is not None:
            params['phone_count']=phone_count

        if phone_number is not None:
            params['phone_number']=self._serialize_list(phone_number)

        if country_state is not None:
            params['country_state']=country_state

        if regulation_address_id is not None:
            params['regulation_address_id']=regulation_address_id

        
        res = self._perform_request('AttachPhoneNumber', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def bind_phone_number_to_application(self, phone_id=None, phone_number=None, application_id=None, application_name=None, rule_id=None, rule_name=None, bind=None):
        """
        Bind the phone number to the application or unbind the phone number from the application. You should specify the application_id or application_name if you specify the rule_name.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if phone_id is not None:
            passed_args.append('phone_id')
        if phone_number is not None:
            passed_args.append('phone_number')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_phone_number_to_application")
        if len(passed_args) == 0:
            raise VoximplantException("None of phone_id, phone_number passed into bind_phone_number_to_application")
        
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_phone_number_to_application")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into bind_phone_number_to_application")
        
        
        passed_args = []
        if rule_id is not None:
            passed_args.append('rule_id')
        if rule_name is not None:
            passed_args.append('rule_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_phone_number_to_application")
        
        
        
        if phone_id is not None:
            params['phone_id']=self._serialize_list(phone_id)

        if phone_number is not None:
            params['phone_number']=self._serialize_list(phone_number)

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if rule_id is not None:
            params['rule_id']=rule_id

        if rule_name is not None:
            params['rule_name']=rule_name

        if bind is not None:
            params['bind']=bind

        
        res = self._perform_request('BindPhoneNumberToApplication', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def deactivate_phone_number(self, phone_id=None, phone_number=None):
        """
        Deactivates the phone number.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if phone_id is not None:
            passed_args.append('phone_id')
        if phone_number is not None:
            passed_args.append('phone_number')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into deactivate_phone_number")
        if len(passed_args) == 0:
            raise VoximplantException("None of phone_id, phone_number passed into deactivate_phone_number")
        
        
        
        if phone_id is not None:
            params['phone_id']=self._serialize_list(phone_id)

        if phone_number is not None:
            params['phone_number']=self._serialize_list(phone_number)

        
        res = self._perform_request('DeactivatePhoneNumber', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_phone_number_info(self, phone_id=None, phone_number=None, incoming_sms_callback_url=None):
        """
        Set the phone number information.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if phone_id is not None:
            passed_args.append('phone_id')
        if phone_number is not None:
            passed_args.append('phone_number')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_phone_number_info")
        if len(passed_args) == 0:
            raise VoximplantException("None of phone_id, phone_number passed into set_phone_number_info")
        
        
        
        if phone_id is not None:
            params['phone_id']=self._serialize_list(phone_id)

        if phone_number is not None:
            params['phone_number']=self._serialize_list(phone_number)

        if incoming_sms_callback_url is not None:
            params['incoming_sms_callback_url']=incoming_sms_callback_url

        
        res = self._perform_request('SetPhoneNumberInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_phone_numbers(self, phone_id=None, phone_number=None, application_id=None, application_name=None, is_bound_to_application=None, phone_template=None, country_code=None, phone_category_name=None, canceled=None, deactivated=None, auto_charge=None, from_phone_next_renewal=None, to_phone_next_renewal=None, from_phone_purchase_date=None, to_phone_purchase_date=None, child_account_id=None, children_phones_only=None, verification_name=None, verification_status=None, from_unverified_hold_until=None, to_unverified_hold_until=None, can_be_used=None, order_by=None, sandbox=None, count=None, offset=None, phone_region_name=None, rule_id=None, rule_name=None, is_bound_to_rule=None):
        """
        Gets the account phone numbers.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_phone_numbers")
        
        
        
        if phone_id is not None:
            params['phone_id']=self._serialize_list(phone_id)

        if phone_number is not None:
            params['phone_number']=self._serialize_list(phone_number)

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if is_bound_to_application is not None:
            params['is_bound_to_application']=is_bound_to_application

        if phone_template is not None:
            params['phone_template']=phone_template

        if country_code is not None:
            params['country_code']=self._serialize_list(country_code)

        if phone_category_name is not None:
            params['phone_category_name']=phone_category_name

        if canceled is not None:
            params['canceled']=canceled

        if deactivated is not None:
            params['deactivated']=deactivated

        if auto_charge is not None:
            params['auto_charge']=auto_charge

        if from_phone_next_renewal is not None:
            params['from_phone_next_renewal']=from_phone_next_renewal

        if to_phone_next_renewal is not None:
            params['to_phone_next_renewal']=to_phone_next_renewal

        if from_phone_purchase_date is not None:
            params['from_phone_purchase_date']=self._py_datetime_to_api(from_phone_purchase_date)

        if to_phone_purchase_date is not None:
            params['to_phone_purchase_date']=self._py_datetime_to_api(to_phone_purchase_date)

        if child_account_id is not None:
            params['child_account_id']=self._serialize_list(child_account_id)

        if children_phones_only is not None:
            params['children_phones_only']=children_phones_only

        if verification_name is not None:
            params['verification_name']=verification_name

        if verification_status is not None:
            params['verification_status']=self._serialize_list(verification_status)

        if from_unverified_hold_until is not None:
            params['from_unverified_hold_until']=from_unverified_hold_until

        if to_unverified_hold_until is not None:
            params['to_unverified_hold_until']=to_unverified_hold_until

        if can_be_used is not None:
            params['can_be_used']=can_be_used

        if order_by is not None:
            params['order_by']=order_by

        if sandbox is not None:
            params['sandbox']=sandbox

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if phone_region_name is not None:
            params['phone_region_name']=self._serialize_list(phone_region_name)

        if rule_id is not None:
            params['rule_id']=self._serialize_list(rule_id)

        if rule_name is not None:
            params['rule_name']=self._serialize_list(rule_name)

        if is_bound_to_rule is not None:
            params['is_bound_to_rule']=is_bound_to_rule

        
        res = self._perform_request('GetPhoneNumbers', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_attached_phone_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_new_phone_numbers(self, country_code, phone_category_name, phone_region_id, country_state=None, count=None, offset=None, phone_number_mask=None):
        """
        Gets the new phone numbers.

        
        :rtype: dict
        """
        params = dict()
        
        params['country_code']=country_code

        params['phone_category_name']=phone_category_name

        params['phone_region_id']=phone_region_id

        
        if country_state is not None:
            params['country_state']=country_state

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if phone_number_mask is not None:
            params['phone_number_mask']=phone_number_mask

        
        res = self._perform_request('GetNewPhoneNumbers', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_new_phone_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_phone_number_categories(self, country_code=None, sandbox=None, locale=None):
        """
        Gets the phone number categories.

        
        :rtype: dict
        """
        params = dict()
        
        
        if country_code is not None:
            params['country_code']=self._serialize_list(country_code)

        if sandbox is not None:
            params['sandbox']=sandbox

        if locale is not None:
            params['locale']=locale

        
        res = self._perform_request('GetPhoneNumberCategories', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_phone_number_country_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_phone_number_country_states(self, country_code, phone_category_name, country_state=None):
        """
        Gets the phone number country states.

        
        :rtype: dict
        """
        params = dict()
        
        params['country_code']=country_code

        params['phone_category_name']=phone_category_name

        
        if country_state is not None:
            params['country_state']=country_state

        
        res = self._perform_request('GetPhoneNumberCountryStates', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_phone_number_country_state_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_phone_number_regions(self, country_code, phone_category_name, country_state=None, omit_empty=None, phone_region_id=None, phone_region_name=None, phone_region_code=None, locale=None):
        """
        Get the country regions of the phone numbers. The response also contains the info about multiple numbers subscription for the child accounts.

        
        :rtype: dict
        """
        params = dict()
        
        params['country_code']=country_code

        params['phone_category_name']=phone_category_name

        
        if country_state is not None:
            params['country_state']=country_state

        if omit_empty is not None:
            params['omit_empty']=omit_empty

        if phone_region_id is not None:
            params['phone_region_id']=phone_region_id

        if phone_region_name is not None:
            params['phone_region_name']=phone_region_name

        if phone_region_code is not None:
            params['phone_region_code']=phone_region_code

        if locale is not None:
            params['locale']=locale

        
        res = self._perform_request('GetPhoneNumberRegions', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_phone_number_country_region_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_actual_phone_number_region(self, country_code, phone_category_name, phone_region_id, country_state=None, locale=None):
        """
        Get actual info on the country region of the phone numbers. The response also contains the info about multiple numbers subscription for the child accounts.

        
        :rtype: dict
        """
        params = dict()
        
        params['country_code']=country_code

        params['phone_category_name']=phone_category_name

        params['phone_region_id']=phone_region_id

        
        if country_state is not None:
            params['country_state']=country_state

        if locale is not None:
            params['locale']=locale

        
        res = self._perform_request('GetActualPhoneNumberRegion', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_phone_number_country_region_info_type(res["result"])
        
        return res

    def add_caller_id(self, callerid_number):
        """
        Adds a new caller ID. Caller ID is the phone that is displayed to the called user. This number can be used for call back.

        
        :rtype: dict
        """
        params = dict()
        
        params['callerid_number']=callerid_number

        
        
        res = self._perform_request('AddCallerID', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def activate_caller_id(self, verification_code, callerid_id=None, callerid_number=None):
        """
        Activates the CallerID by the verification code.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if callerid_id is not None:
            passed_args.append('callerid_id')
        if callerid_number is not None:
            passed_args.append('callerid_number')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into activate_caller_id")
        if len(passed_args) == 0:
            raise VoximplantException("None of callerid_id, callerid_number passed into activate_caller_id")
        
        
        params['verification_code']=verification_code

        
        if callerid_id is not None:
            params['callerid_id']=callerid_id

        if callerid_number is not None:
            params['callerid_number']=callerid_number

        
        res = self._perform_request('ActivateCallerID', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_caller_id(self, callerid_id=None, callerid_number=None):
        """
        Deletes the CallerID. Note: you cannot delete a CID permanently (the antispam defence).

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if callerid_id is not None:
            passed_args.append('callerid_id')
        if callerid_number is not None:
            passed_args.append('callerid_number')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_caller_id")
        if len(passed_args) == 0:
            raise VoximplantException("None of callerid_id, callerid_number passed into del_caller_id")
        
        
        
        if callerid_id is not None:
            params['callerid_id']=callerid_id

        if callerid_number is not None:
            params['callerid_number']=callerid_number

        
        res = self._perform_request('DelCallerID', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_caller_ids(self, callerid_id=None, callerid_number=None, active=None, order_by=None, count=None, offset=None):
        """
        Gets the account callerIDs.

        
        :rtype: dict
        """
        params = dict()
        
        
        if callerid_id is not None:
            params['callerid_id']=callerid_id

        if callerid_number is not None:
            params['callerid_number']=callerid_number

        if active is not None:
            params['active']=active

        if order_by is not None:
            params['order_by']=order_by

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetCallerIDs', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_caller_id_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def verify_caller_id(self, callerid_id=None, callerid_number=None):
        """
        Gets a verification code via phone call to the **callerid_number**.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if callerid_id is not None:
            passed_args.append('callerid_id')
        if callerid_number is not None:
            passed_args.append('callerid_number')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into verify_caller_id")
        if len(passed_args) == 0:
            raise VoximplantException("None of callerid_id, callerid_number passed into verify_caller_id")
        
        
        
        if callerid_id is not None:
            params['callerid_id']=callerid_id

        if callerid_number is not None:
            params['callerid_number']=callerid_number

        
        res = self._perform_request('VerifyCallerID', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def add_outbound_test_phone_number(self, phone_number):
        """
        Adds a personal phone number to test outgoing calls. Only one personal phone number can be used. To replace it with another, delete the existing one first.

        
        :rtype: dict
        """
        params = dict()
        
        params['phone_number']=phone_number

        
        
        res = self._perform_request('AddOutboundTestPhoneNumber', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def verify_outbound_test_phone_number(self):
        """
        Starts a call to the added phone number and pronounces a verification code. You have only 5 verification attempts per day and 100 in total. 1 minute should pass between 2 attempts.

        
        :rtype: dict
        """
        params = dict()
        
        
        
        res = self._perform_request('VerifyOutboundTestPhoneNumber', params)
        
        return res

    def activate_outbound_test_phone_number(self, verification_code):
        """
        Activates the phone number by the verification code.

        
        :rtype: dict
        """
        params = dict()
        
        params['verification_code']=verification_code

        
        
        res = self._perform_request('ActivateOutboundTestPhoneNumber', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_outbound_test_phone_number(self):
        """
        Deletes the existing phone number.

        
        :rtype: dict
        """
        params = dict()
        
        
        
        res = self._perform_request('DelOutboundTestPhoneNumber', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_outbound_test_phone_numbers(self):
        """
        Shows the phone number info.

        
        :rtype: dict
        """
        params = dict()
        
        
        
        res = self._perform_request('GetOutboundTestPhoneNumbers', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_outbound_test_phonenumber_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def add_queue(self, acd_queue_name, application_id=None, application_name=None, acd_queue_priority=None, auto_binding=None, service_probability=None, max_queue_size=None, max_waiting_time=None, average_service_time=None):
        """
        Adds a new ACD queue.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_queue")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into add_queue")
        
        
        params['acd_queue_name']=acd_queue_name

        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if acd_queue_priority is not None:
            params['acd_queue_priority']=acd_queue_priority

        if auto_binding is not None:
            params['auto_binding']=auto_binding

        if service_probability is not None:
            params['service_probability']=service_probability

        if max_queue_size is not None:
            params['max_queue_size']=max_queue_size

        if max_waiting_time is not None:
            params['max_waiting_time']=max_waiting_time

        if average_service_time is not None:
            params['average_service_time']=average_service_time

        
        res = self._perform_request('AddQueue', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def bind_user_to_queue(self, bind, application_id=None, application_name=None, user_id=None, user_name=None, acd_queue_id=None, acd_queue_name=None):
        """
        Bind/unbind users to/from the specified ACD queues. Note that users and queues should be already bound to the same application.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_user_to_queue")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into bind_user_to_queue")
        
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_user_to_queue")
        if len(passed_args) == 0:
            raise VoximplantException("None of user_id, user_name passed into bind_user_to_queue")
        
        
        passed_args = []
        if acd_queue_id is not None:
            passed_args.append('acd_queue_id')
        if acd_queue_name is not None:
            passed_args.append('acd_queue_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_user_to_queue")
        if len(passed_args) == 0:
            raise VoximplantException("None of acd_queue_id, acd_queue_name passed into bind_user_to_queue")
        
        
        params['bind']=bind

        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if acd_queue_id is not None:
            params['acd_queue_id']=self._serialize_list(acd_queue_id)

        if acd_queue_name is not None:
            params['acd_queue_name']=self._serialize_list(acd_queue_name)

        
        res = self._perform_request('BindUserToQueue', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_queue(self, acd_queue_id=None, acd_queue_name=None):
        """
        Deletes the ACD queue.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if acd_queue_id is not None:
            passed_args.append('acd_queue_id')
        if acd_queue_name is not None:
            passed_args.append('acd_queue_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_queue")
        if len(passed_args) == 0:
            raise VoximplantException("None of acd_queue_id, acd_queue_name passed into del_queue")
        
        
        
        if acd_queue_id is not None:
            params['acd_queue_id']=self._serialize_list(acd_queue_id)

        if acd_queue_name is not None:
            params['acd_queue_name']=self._serialize_list(acd_queue_name)

        
        res = self._perform_request('DelQueue', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_queue_info(self, acd_queue_id=None, acd_queue_name=None, new_acd_queue_name=None, acd_queue_priority=None, auto_binding=None, service_probability=None, max_queue_size=None, max_waiting_time=None, average_service_time=None, application_id=None):
        """
        Edits the ACD queue.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if acd_queue_id is not None:
            passed_args.append('acd_queue_id')
        if acd_queue_name is not None:
            passed_args.append('acd_queue_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_queue_info")
        if len(passed_args) == 0:
            raise VoximplantException("None of acd_queue_id, acd_queue_name passed into set_queue_info")
        
        
        
        if acd_queue_id is not None:
            params['acd_queue_id']=acd_queue_id

        if acd_queue_name is not None:
            params['acd_queue_name']=acd_queue_name

        if new_acd_queue_name is not None:
            params['new_acd_queue_name']=new_acd_queue_name

        if acd_queue_priority is not None:
            params['acd_queue_priority']=acd_queue_priority

        if auto_binding is not None:
            params['auto_binding']=auto_binding

        if service_probability is not None:
            params['service_probability']=service_probability

        if max_queue_size is not None:
            params['max_queue_size']=max_queue_size

        if max_waiting_time is not None:
            params['max_waiting_time']=max_waiting_time

        if average_service_time is not None:
            params['average_service_time']=average_service_time

        if application_id is not None:
            params['application_id']=application_id

        
        res = self._perform_request('SetQueueInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_queues(self, acd_queue_id=None, acd_queue_name=None, application_id=None, skill_id=None, excluded_skill_id=None, with_skills=None, showing_skill_id=None, count=None, offset=None, with_operatorcount=None):
        """
        Gets the ACD queues.

        
        :rtype: dict
        """
        params = dict()
        
        
        if acd_queue_id is not None:
            params['acd_queue_id']=acd_queue_id

        if acd_queue_name is not None:
            params['acd_queue_name']=acd_queue_name

        if application_id is not None:
            params['application_id']=application_id

        if skill_id is not None:
            params['skill_id']=skill_id

        if excluded_skill_id is not None:
            params['excluded_skill_id']=excluded_skill_id

        if with_skills is not None:
            params['with_skills']=with_skills

        if showing_skill_id is not None:
            params['showing_skill_id']=showing_skill_id

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if with_operatorcount is not None:
            params['with_operatorcount']=with_operatorcount

        
        res = self._perform_request('GetQueues', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_queue_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_acd_state(self, acd_queue_id=None):
        """
        Gets the current ACD queue state.

        
        :rtype: dict
        """
        params = dict()
        
        
        if acd_queue_id is not None:
            params['acd_queue_id']=self._serialize_list(acd_queue_id)

        
        res = self._perform_request('GetACDState', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_acd_state_type(res["result"])
        
        return res

    def get_acd_operator_statistics(self, from_date, user_id, to_date=None, acd_queue_id=None, abbreviation=None, report=None, aggregation=None, group=None):
        """
        Get statistics for calls distributed to users (referred as 'operators') via the 'ACD' module. This method can filter statistic based on operator ids, queue ids and date-time interval. It can also group results by day or hour.

        
        :rtype: dict
        """
        params = dict()
        
        params['from_date']=self._py_datetime_to_api(from_date)

        params['user_id']=self._serialize_list(user_id)

        
        if to_date is not None:
            params['to_date']=self._py_datetime_to_api(to_date)

        if acd_queue_id is not None:
            params['acd_queue_id']=self._serialize_list(acd_queue_id)

        if abbreviation is not None:
            params['abbreviation']=abbreviation

        if report is not None:
            params['report']=self._serialize_list(report)

        if aggregation is not None:
            params['aggregation']=aggregation

        if group is not None:
            params['group']=group

        
        res = self._perform_request('GetACDOperatorStatistics', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_acd_operator_aggregation_group_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_acd_queue_statistics(self, from_date, to_date=None, abbreviation=None, acd_queue_id=None, report=None, aggregation=None):
        """
        Get statistics for calls distributed to users (referred as 'operators') via the 'queue' distribution system. This method can filter statistic based on operator ids, queue ids and date-time interval. It can also group results by day or hour.

        
        :rtype: dict
        """
        params = dict()
        
        params['from_date']=self._py_datetime_to_api(from_date)

        
        if to_date is not None:
            params['to_date']=self._py_datetime_to_api(to_date)

        if abbreviation is not None:
            params['abbreviation']=abbreviation

        if acd_queue_id is not None:
            params['acd_queue_id']=self._serialize_list(acd_queue_id)

        if report is not None:
            params['report']=self._serialize_list(report)

        if aggregation is not None:
            params['aggregation']=aggregation

        
        res = self._perform_request('GetACDQueueStatistics', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_acd_queue_statistics_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_acd_operator_status_statistics(self, from_date, user_id, to_date=None, acd_status=None, aggregation=None, group=None):
        """
        Get statistics for the specified operators and ACD statuses. This method can filter statistics by operator ids and statuses. It can also group results by day/hour or users.

        
        :rtype: dict
        """
        params = dict()
        
        params['from_date']=self._py_datetime_to_api(from_date)

        params['user_id']=self._serialize_list(user_id)

        
        if to_date is not None:
            params['to_date']=self._py_datetime_to_api(to_date)

        if acd_status is not None:
            params['acd_status']=self._serialize_list(acd_status)

        if aggregation is not None:
            params['aggregation']=aggregation

        if group is not None:
            params['group']=group

        
        res = self._perform_request('GetACDOperatorStatusStatistics', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_acd_operator_status_aggregation_group_type(p)
            except TypeError as te:
                pass
        
        return res

    def get_smart_queue_realtime_metrics(self, report_type, application_id=None, application_name=None, user_id=None, user_name=None, sq_queue_name=None, from_date=None, to_date=None, timezone=None, interval=None, group_by=None, max_waiting_sec=None):
        """
        Gets the metrics for the specified SmartQueue for the last 30 minutes. Refer to the <a href="/docs/guides/contact-center/reporting">SmartQueue reporting guide</a> to learn more.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_smart_queue_realtime_metrics")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into get_smart_queue_realtime_metrics")
        
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_smart_queue_realtime_metrics")
        
        
        passed_args = []
        if sq_queue_name is not None:
            passed_args.append('sq_queue_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_smart_queue_realtime_metrics")
        
        
        params['report_type']=self._serialize_list(report_type)

        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if sq_queue_name is not None:
            params['sq_queue_name']=self._serialize_list(sq_queue_name)

        if from_date is not None:
            params['from_date']=self._py_datetime_to_api(from_date)

        if to_date is not None:
            params['to_date']=self._py_datetime_to_api(to_date)

        if timezone is not None:
            params['timezone']=timezone

        if interval is not None:
            params['interval']=interval

        if group_by is not None:
            params['group_by']=group_by

        if max_waiting_sec is not None:
            params['max_waiting_sec']=max_waiting_sec

        
        res = self._perform_request('GetSmartQueueRealtimeMetrics', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_smart_queue_metrics_result(p)
            except TypeError as te:
                pass
        
        return res

    def get_smart_queue_day_history(self, report_type, application_id=None, application_name=None, user_id=None, user_name=None, sq_queue_id=None, sq_queue_name=None, from_date=None, to_date=None, timezone=None, interval=None, group_by=None, max_waiting_sec=None):
        """
        Gets the metrics for the specified SmartQueue for the last 2 days. Refer to the <a href="/docs/guides/contact-center/reporting">SmartQueue reporting guide</a> to learn more.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_smart_queue_day_history")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into get_smart_queue_day_history")
        
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_smart_queue_day_history")
        
        
        passed_args = []
        if sq_queue_id is not None:
            passed_args.append('sq_queue_id')
        if sq_queue_name is not None:
            passed_args.append('sq_queue_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_smart_queue_day_history")
        if len(passed_args) == 0:
            raise VoximplantException("None of sq_queue_id, sq_queue_name passed into get_smart_queue_day_history")
        
        
        params['report_type']=self._serialize_list(report_type)

        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if sq_queue_id is not None:
            params['sq_queue_id']=self._serialize_list(sq_queue_id)

        if sq_queue_name is not None:
            params['sq_queue_name']=self._serialize_list(sq_queue_name)

        if from_date is not None:
            params['from_date']=self._py_datetime_to_api(from_date)

        if to_date is not None:
            params['to_date']=self._py_datetime_to_api(to_date)

        if timezone is not None:
            params['timezone']=timezone

        if interval is not None:
            params['interval']=interval

        if group_by is not None:
            params['group_by']=group_by

        if max_waiting_sec is not None:
            params['max_waiting_sec']=max_waiting_sec

        
        res = self._perform_request('GetSmartQueueDayHistory', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_smart_queue_metrics_result(p)
            except TypeError as te:
                pass
        
        return res

    def request_smart_queue_history(self, from_date, to_date, report_type, application_id=None, application_name=None, user_id=None, user_name=None, sq_queue_id=None, sq_queue_name=None, timezone=None, interval=None, group_by=None, max_waiting_sec=None):
        """
        Gets history for the specified SmartQueue. Refer to the <a href="/docs/guides/contact-center/reporting">SmartQueue reporting guide</a> to learn more.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into request_smart_queue_history")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into request_smart_queue_history")
        
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into request_smart_queue_history")
        
        
        passed_args = []
        if sq_queue_id is not None:
            passed_args.append('sq_queue_id')
        if sq_queue_name is not None:
            passed_args.append('sq_queue_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into request_smart_queue_history")
        if len(passed_args) == 0:
            raise VoximplantException("None of sq_queue_id, sq_queue_name passed into request_smart_queue_history")
        
        
        params['from_date']=self._py_datetime_to_api(from_date)

        params['to_date']=self._py_datetime_to_api(to_date)

        params['report_type']=self._serialize_list(report_type)

        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if sq_queue_id is not None:
            params['sq_queue_id']=self._serialize_list(sq_queue_id)

        if sq_queue_name is not None:
            params['sq_queue_name']=self._serialize_list(sq_queue_name)

        if timezone is not None:
            params['timezone']=timezone

        if interval is not None:
            params['interval']=interval

        if group_by is not None:
            params['group_by']=group_by

        if max_waiting_sec is not None:
            params['max_waiting_sec']=max_waiting_sec

        
        res = self._perform_request('RequestSmartQueueHistory', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_sq_state(self, application_id=None, application_name=None, sq_queue_id=None, sq_queue_name=None, timezone=None):
        """
        Gets the current state of the specified SmartQueue.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_sq_state")
        if len(passed_args) == 0:
            raise VoximplantException("None of application_id, application_name passed into get_sq_state")
        
        
        passed_args = []
        if sq_queue_id is not None:
            passed_args.append('sq_queue_id')
        if sq_queue_name is not None:
            passed_args.append('sq_queue_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into get_sq_state")
        if len(passed_args) == 0:
            raise VoximplantException("None of sq_queue_id, sq_queue_name passed into get_sq_state")
        
        
        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if sq_queue_id is not None:
            params['sq_queue_id']=self._serialize_list(sq_queue_id)

        if sq_queue_name is not None:
            params['sq_queue_name']=self._serialize_list(sq_queue_name)

        if timezone is not None:
            params['timezone']=timezone

        
        res = self._perform_request('GetSQState', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_smart_queue_state(p)
            except TypeError as te:
                pass
        
        return res

    def sq__set_agent_custom_status_mapping(self, sq_status_name, custom_status_name, application_id):
        """
        Adds a status if there is no match for the given internal status and renames it if there is a match. It means that if the passed **sq_status_name** parameter is not in the mapping table, a new entry is created in there; if it is, the **name** field in its mapping is replaced with **custom_status_name**.

        
        :rtype: dict
        """
        params = dict()
        
        params['sq_status_name']=sq_status_name

        params['custom_status_name']=custom_status_name

        params['application_id']=application_id

        
        
        res = self._perform_request('SQ_SetAgentCustomStatusMapping', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def sq__get_agent_custom_status_mapping(self, application_id=None):
        """
        Returns the mapping list of SQ statuses and custom statuses. SQ statuses are returned whether or not they have mappings to custom statuses.

        
        :rtype: dict
        """
        params = dict()
        
        
        if application_id is not None:
            params['application_id']=application_id

        
        res = self._perform_request('SQ_GetAgentCustomStatusMapping', params)
        
        return res

    def sq__delete_agent_custom_status_mapping(self, application_id, sq_status_name=None):
        """
        Removes a mapping from the mapping table. If there is no such mapping, does nothing.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        
        if sq_status_name is not None:
            params['sq_status_name']=sq_status_name

        
        res = self._perform_request('SQ_DeleteAgentCustomStatusMapping', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def add_skill(self, skill_name):
        """
        Adds a new operator's skill. Works only for ACDv1. For SmartQueue/ACDv2, use <a href="#how-auth-works">this reference</a>.

        
        :rtype: dict
        """
        params = dict()
        
        params['skill_name']=skill_name

        
        
        res = self._perform_request('AddSkill', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_skill(self, skill_id=None, skill_name=None):
        """
        Deletes an operator's skill. Works only for ACDv1. For SmartQueue/ACDv2, use <a href="#how-auth-works">this reference</a>.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if skill_id is not None:
            passed_args.append('skill_id')
        if skill_name is not None:
            passed_args.append('skill_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_skill")
        if len(passed_args) == 0:
            raise VoximplantException("None of skill_id, skill_name passed into del_skill")
        
        
        
        if skill_id is not None:
            params['skill_id']=skill_id

        if skill_name is not None:
            params['skill_name']=skill_name

        
        res = self._perform_request('DelSkill', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_skill_info(self, new_skill_name, skill_id=None, skill_name=None):
        """
        Edits an operator's skill. Works only for ACDv1. For SmartQueue/ACDv2, use <a href="#how-auth-works">this reference</a>.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if skill_id is not None:
            passed_args.append('skill_id')
        if skill_name is not None:
            passed_args.append('skill_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_skill_info")
        if len(passed_args) == 0:
            raise VoximplantException("None of skill_id, skill_name passed into set_skill_info")
        
        
        params['new_skill_name']=new_skill_name

        
        if skill_id is not None:
            params['skill_id']=skill_id

        if skill_name is not None:
            params['skill_name']=skill_name

        
        res = self._perform_request('SetSkillInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_skills(self, skill_id=None, skill_name=None, count=None, offset=None):
        """
        Gets the skills of an operator. Works only for ACDv1. For SmartQueue/ACDv2, use <a href="#how-auth-works">this reference</a>.

        
        :rtype: dict
        """
        params = dict()
        
        
        if skill_id is not None:
            params['skill_id']=skill_id

        if skill_name is not None:
            params['skill_name']=skill_name

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetSkills', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_skill_info_type(p)
            except TypeError as te:
                pass
        
        return res

    def bind_skill(self, skill_id=None, skill_name=None, user_id=None, user_name=None, acd_queue_id=None, acd_queue_name=None, application_id=None, application_name=None, bind=None):
        """
        Binds the specified skills to the users (ACD operators) and/or the ACD queues. Works only for ACDv1. For SmartQueue/ACDv2, use <a href="#how-auth-works">this reference</a>.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if skill_id is not None:
            passed_args.append('skill_id')
        if skill_name is not None:
            passed_args.append('skill_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_skill")
        if len(passed_args) == 0:
            raise VoximplantException("None of skill_id, skill_name passed into bind_skill")
        
        
        passed_args = []
        if user_id is not None:
            passed_args.append('user_id')
        if user_name is not None:
            passed_args.append('user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_skill")
        if len(passed_args) == 0:
            raise VoximplantException("None of user_id, user_name passed into bind_skill")
        
        
        passed_args = []
        if acd_queue_id is not None:
            passed_args.append('acd_queue_id')
        if acd_queue_name is not None:
            passed_args.append('acd_queue_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_skill")
        if len(passed_args) == 0:
            raise VoximplantException("None of acd_queue_id, acd_queue_name passed into bind_skill")
        
        
        passed_args = []
        if application_id is not None:
            passed_args.append('application_id')
        if application_name is not None:
            passed_args.append('application_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into bind_skill")
        
        
        
        if skill_id is not None:
            params['skill_id']=self._serialize_list(skill_id)

        if skill_name is not None:
            params['skill_name']=self._serialize_list(skill_name)

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if acd_queue_id is not None:
            params['acd_queue_id']=self._serialize_list(acd_queue_id)

        if acd_queue_name is not None:
            params['acd_queue_name']=self._serialize_list(acd_queue_name)

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if bind is not None:
            params['bind']=bind

        
        res = self._perform_request('BindSkill', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_account_documents(self, with_details=None, verification_name=None, verification_status=None, from_unverified_hold_until=None, to_unverified_hold_until=None, child_account_id=None, children_verifications_only=None):
        """
        Gets the account documents and the verification states.

        
        :rtype: dict
        """
        params = dict()
        
        
        if with_details is not None:
            params['with_details']=with_details

        if verification_name is not None:
            params['verification_name']=verification_name

        if verification_status is not None:
            params['verification_status']=self._serialize_list(verification_status)

        if from_unverified_hold_until is not None:
            params['from_unverified_hold_until']=from_unverified_hold_until

        if to_unverified_hold_until is not None:
            params['to_unverified_hold_until']=to_unverified_hold_until

        if child_account_id is not None:
            params['child_account_id']=self._serialize_list(child_account_id)

        if children_verifications_only is not None:
            params['children_verifications_only']=children_verifications_only

        
        res = self._perform_request('GetAccountDocuments', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_account_verifications(p)
            except TypeError as te:
                pass
        
        return res

    def add_admin_user(self, new_admin_user_name, admin_user_display_name, new_admin_user_password, admin_user_active=None, admin_role_id=None, admin_role_name=None):
        """
        Adds a new admin user into the specified parent or child account.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if admin_role_id is not None:
            passed_args.append('admin_role_id')
        if admin_role_name is not None:
            passed_args.append('admin_role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_admin_user")
        
        
        params['new_admin_user_name']=new_admin_user_name

        params['admin_user_display_name']=admin_user_display_name

        params['new_admin_user_password']=new_admin_user_password

        
        if admin_user_active is not None:
            params['admin_user_active']=admin_user_active

        if admin_role_id is not None:
            params['admin_role_id']=admin_role_id

        if admin_role_name is not None:
            params['admin_role_name']=self._serialize_list(admin_role_name)

        
        res = self._perform_request('AddAdminUser', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_admin_user(self, required_admin_user_id=None, required_admin_user_name=None):
        """
        Deletes the specified admin user.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if required_admin_user_id is not None:
            passed_args.append('required_admin_user_id')
        if required_admin_user_name is not None:
            passed_args.append('required_admin_user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_admin_user")
        if len(passed_args) == 0:
            raise VoximplantException("None of required_admin_user_id, required_admin_user_name passed into del_admin_user")
        
        
        
        if required_admin_user_id is not None:
            params['required_admin_user_id']=self._serialize_list(required_admin_user_id)

        if required_admin_user_name is not None:
            params['required_admin_user_name']=self._serialize_list(required_admin_user_name)

        
        res = self._perform_request('DelAdminUser', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_admin_user_info(self, required_admin_user_id=None, required_admin_user_name=None, new_admin_user_name=None, admin_user_display_name=None, new_admin_user_password=None, admin_user_active=None):
        """
        Edits the specified admin user.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if required_admin_user_id is not None:
            passed_args.append('required_admin_user_id')
        if required_admin_user_name is not None:
            passed_args.append('required_admin_user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_admin_user_info")
        if len(passed_args) == 0:
            raise VoximplantException("None of required_admin_user_id, required_admin_user_name passed into set_admin_user_info")
        
        
        
        if required_admin_user_id is not None:
            params['required_admin_user_id']=required_admin_user_id

        if required_admin_user_name is not None:
            params['required_admin_user_name']=required_admin_user_name

        if new_admin_user_name is not None:
            params['new_admin_user_name']=new_admin_user_name

        if admin_user_display_name is not None:
            params['admin_user_display_name']=admin_user_display_name

        if new_admin_user_password is not None:
            params['new_admin_user_password']=new_admin_user_password

        if admin_user_active is not None:
            params['admin_user_active']=admin_user_active

        
        res = self._perform_request('SetAdminUserInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_admin_users(self, required_admin_user_id=None, required_admin_user_name=None, admin_user_display_name=None, admin_user_active=None, with_roles=None, with_access_entries=None, count=None, offset=None):
        """
        Gets the admin users of the specified account. Note that both account types - parent and child - can have its own admins.

        
        :rtype: dict
        """
        params = dict()
        
        
        if required_admin_user_id is not None:
            params['required_admin_user_id']=required_admin_user_id

        if required_admin_user_name is not None:
            params['required_admin_user_name']=required_admin_user_name

        if admin_user_display_name is not None:
            params['admin_user_display_name']=admin_user_display_name

        if admin_user_active is not None:
            params['admin_user_active']=admin_user_active

        if with_roles is not None:
            params['with_roles']=with_roles

        if with_access_entries is not None:
            params['with_access_entries']=with_access_entries

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetAdminUsers', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_admin_user_type(p)
            except TypeError as te:
                pass
        
        return res

    def add_admin_role(self, admin_role_name, admin_role_active=None, like_admin_role_id=None, like_admin_role_name=None, allowed_entries=None, denied_entries=None):
        """
        Adds a new admin role.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if like_admin_role_id is not None:
            passed_args.append('like_admin_role_id')
        if like_admin_role_name is not None:
            passed_args.append('like_admin_role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_admin_role")
        
        
        params['admin_role_name']=admin_role_name

        
        if admin_role_active is not None:
            params['admin_role_active']=admin_role_active

        if like_admin_role_id is not None:
            params['like_admin_role_id']=self._serialize_list(like_admin_role_id)

        if like_admin_role_name is not None:
            params['like_admin_role_name']=self._serialize_list(like_admin_role_name)

        if allowed_entries is not None:
            params['allowed_entries']=self._serialize_list(allowed_entries)

        if denied_entries is not None:
            params['denied_entries']=self._serialize_list(denied_entries)

        
        res = self._perform_request('AddAdminRole', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_admin_role(self, admin_role_id=None, admin_role_name=None):
        """
        Deletes the specified admin role.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if admin_role_id is not None:
            passed_args.append('admin_role_id')
        if admin_role_name is not None:
            passed_args.append('admin_role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_admin_role")
        if len(passed_args) == 0:
            raise VoximplantException("None of admin_role_id, admin_role_name passed into del_admin_role")
        
        
        
        if admin_role_id is not None:
            params['admin_role_id']=self._serialize_list(admin_role_id)

        if admin_role_name is not None:
            params['admin_role_name']=self._serialize_list(admin_role_name)

        
        res = self._perform_request('DelAdminRole', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_admin_role_info(self, admin_role_id=None, admin_role_name=None, new_admin_role_name=None, admin_role_active=None, entry_modification_mode=None, allowed_entries=None, denied_entries=None, like_admin_role_id=None, like_admin_role_name=None):
        """
        Edits the specified admin role.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if admin_role_id is not None:
            passed_args.append('admin_role_id')
        if admin_role_name is not None:
            passed_args.append('admin_role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_admin_role_info")
        if len(passed_args) == 0:
            raise VoximplantException("None of admin_role_id, admin_role_name passed into set_admin_role_info")
        
        
        passed_args = []
        if like_admin_role_id is not None:
            passed_args.append('like_admin_role_id')
        if like_admin_role_name is not None:
            passed_args.append('like_admin_role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_admin_role_info")
        
        
        
        if admin_role_id is not None:
            params['admin_role_id']=admin_role_id

        if admin_role_name is not None:
            params['admin_role_name']=admin_role_name

        if new_admin_role_name is not None:
            params['new_admin_role_name']=new_admin_role_name

        if admin_role_active is not None:
            params['admin_role_active']=admin_role_active

        if entry_modification_mode is not None:
            params['entry_modification_mode']=entry_modification_mode

        if allowed_entries is not None:
            params['allowed_entries']=self._serialize_list(allowed_entries)

        if denied_entries is not None:
            params['denied_entries']=self._serialize_list(denied_entries)

        if like_admin_role_id is not None:
            params['like_admin_role_id']=self._serialize_list(like_admin_role_id)

        if like_admin_role_name is not None:
            params['like_admin_role_name']=self._serialize_list(like_admin_role_name)

        
        res = self._perform_request('SetAdminRoleInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_admin_roles(self, admin_role_id=None, admin_role_name=None, admin_role_active=None, with_entries=None, with_account_roles=None, with_parent_roles=None, included_admin_user_id=None, excluded_admin_user_id=None, full_admin_users_matching=None, showing_admin_user_id=None, count=None, offset=None):
        """
        Gets the admin roles.

        
        :rtype: dict
        """
        params = dict()
        
        
        if admin_role_id is not None:
            params['admin_role_id']=admin_role_id

        if admin_role_name is not None:
            params['admin_role_name']=admin_role_name

        if admin_role_active is not None:
            params['admin_role_active']=admin_role_active

        if with_entries is not None:
            params['with_entries']=with_entries

        if with_account_roles is not None:
            params['with_account_roles']=with_account_roles

        if with_parent_roles is not None:
            params['with_parent_roles']=with_parent_roles

        if included_admin_user_id is not None:
            params['included_admin_user_id']=self._serialize_list(included_admin_user_id)

        if excluded_admin_user_id is not None:
            params['excluded_admin_user_id']=self._serialize_list(excluded_admin_user_id)

        if full_admin_users_matching is not None:
            params['full_admin_users_matching']=full_admin_users_matching

        if showing_admin_user_id is not None:
            params['showing_admin_user_id']=showing_admin_user_id

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetAdminRoles', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_admin_role_type(p)
            except TypeError as te:
                pass
        
        return res

    def attach_admin_role(self, required_admin_user_id=None, required_admin_user_name=None, admin_role_id=None, admin_role_name=None, mode=None):
        """
        Attaches the admin role(s) to the already existing admin(s).

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if required_admin_user_id is not None:
            passed_args.append('required_admin_user_id')
        if required_admin_user_name is not None:
            passed_args.append('required_admin_user_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into attach_admin_role")
        if len(passed_args) == 0:
            raise VoximplantException("None of required_admin_user_id, required_admin_user_name passed into attach_admin_role")
        
        
        passed_args = []
        if admin_role_id is not None:
            passed_args.append('admin_role_id')
        if admin_role_name is not None:
            passed_args.append('admin_role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into attach_admin_role")
        if len(passed_args) == 0:
            raise VoximplantException("None of admin_role_id, admin_role_name passed into attach_admin_role")
        
        
        
        if required_admin_user_id is not None:
            params['required_admin_user_id']=self._serialize_list(required_admin_user_id)

        if required_admin_user_name is not None:
            params['required_admin_user_name']=self._serialize_list(required_admin_user_name)

        if admin_role_id is not None:
            params['admin_role_id']=self._serialize_list(admin_role_id)

        if admin_role_name is not None:
            params['admin_role_name']=self._serialize_list(admin_role_name)

        if mode is not None:
            params['mode']=mode

        
        res = self._perform_request('AttachAdminRole', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_available_admin_role_entries(self):
        """
        Gets the all available admin role entries.

        
        :rtype: dict
        """
        params = dict()
        
        
        
        res = self._perform_request('GetAvailableAdminRoleEntries', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def add_authorized_account_ip(self, authorized_ip, allowed=None, description=None):
        """
        Adds a new authorized IP4 or network to the white/black list.

        
        :rtype: dict
        """
        params = dict()
        
        params['authorized_ip']=authorized_ip

        
        if allowed is not None:
            params['allowed']=allowed

        if description is not None:
            params['description']=description

        
        res = self._perform_request('AddAuthorizedAccountIP', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_authorized_account_ip(self, authorized_ip=None, contains_ip=None, allowed=None):
        """
        Removes the authorized IP4 or network from the white/black list.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if authorized_ip is not None:
            passed_args.append('authorized_ip')
        if contains_ip is not None:
            passed_args.append('contains_ip')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into del_authorized_account_ip")
        if len(passed_args) == 0:
            raise VoximplantException("None of authorized_ip, contains_ip passed into del_authorized_account_ip")
        
        
        
        if authorized_ip is not None:
            params['authorized_ip']=authorized_ip

        if contains_ip is not None:
            params['contains_ip']=contains_ip

        if allowed is not None:
            params['allowed']=allowed

        
        res = self._perform_request('DelAuthorizedAccountIP', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_authorized_account_ips(self, authorized_ip=None, allowed=None, contains_ip=None, count=None, offset=None, description=None):
        """
        Gets the authorized IP4 or network.

        
        :rtype: dict
        """
        params = dict()
        
        
        if authorized_ip is not None:
            params['authorized_ip']=authorized_ip

        if allowed is not None:
            params['allowed']=allowed

        if contains_ip is not None:
            params['contains_ip']=contains_ip

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if description is not None:
            params['description']=description

        
        res = self._perform_request('GetAuthorizedAccountIPs', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_authorized_account_ip_type(p)
            except TypeError as te:
                pass
        
        return res

    def check_authorized_account_ip(self, authorized_ip):
        """
        Tests whether the IP4 is banned or allowed.

        
        :rtype: dict
        """
        params = dict()
        
        params['authorized_ip']=authorized_ip

        
        
        res = self._perform_request('CheckAuthorizedAccountIP', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def link_regulation_address(self, regulation_address_id, phone_id=None, phone_number=None):
        """
        Links the regulation address to a phone.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if phone_id is not None:
            passed_args.append('phone_id')
        if phone_number is not None:
            passed_args.append('phone_number')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into link_regulation_address")
        if len(passed_args) == 0:
            raise VoximplantException("None of phone_id, phone_number passed into link_regulation_address")
        
        
        params['regulation_address_id']=regulation_address_id

        
        if phone_id is not None:
            params['phone_id']=phone_id

        if phone_number is not None:
            params['phone_number']=phone_number

        
        res = self._perform_request('LinkRegulationAddress', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_zip_codes(self, country_code, phone_region_code=None, count=None, offset=None):
        """
        Searches for available zip codes.

        
        :rtype: dict
        """
        params = dict()
        
        params['country_code']=country_code

        
        if phone_region_code is not None:
            params['phone_region_code']=phone_region_code

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetZIPCodes', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_zip_code(p)
            except TypeError as te:
                pass
        
        return res

    def get_regulations_address(self, country_code=None, phone_category_name=None, phone_region_code=None, regulation_address_id=None, verified=None, in_progress=None):
        """
        Searches for the user's regulation address.

        
        :rtype: dict
        """
        params = dict()
        
        
        if country_code is not None:
            params['country_code']=country_code

        if phone_category_name is not None:
            params['phone_category_name']=phone_category_name

        if phone_region_code is not None:
            params['phone_region_code']=phone_region_code

        if regulation_address_id is not None:
            params['regulation_address_id']=regulation_address_id

        if verified is not None:
            params['verified']=verified

        if in_progress is not None:
            params['in_progress']=in_progress

        
        res = self._perform_request('GetRegulationsAddress', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_regulation_address(p)
            except TypeError as te:
                pass
        
        return res

    def get_available_regulations(self, country_code, phone_category_name, phone_region_code=None):
        """
        Searches for the available regulation for a link.

        
        :rtype: dict
        """
        params = dict()
        
        params['country_code']=country_code

        params['phone_category_name']=phone_category_name

        
        if phone_region_code is not None:
            params['phone_region_code']=phone_region_code

        
        res = self._perform_request('GetAvailableRegulations', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_countries(self, country_code=None):
        """
        Gets all countries.

        
        :rtype: dict
        """
        params = dict()
        
        
        if country_code is not None:
            params['country_code']=country_code

        
        res = self._perform_request('GetCountries', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_regulation_country(p)
            except TypeError as te:
                pass
        
        return res

    def get_account_phone_number_countries(self, application_id=None):
        """
        Gets all countries where the specific account has phone numbers.

        
        :rtype: dict
        """
        params = dict()
        
        
        if application_id is not None:
            params['application_id']=self._serialize_list(application_id)

        
        res = self._perform_request('GetAccountPhoneNumberCountries', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_regions(self, country_code, phone_category_name, city_name=None, count=None, offset=None):
        """
        Gets available regions in a country.

        
        :rtype: dict
        """
        params = dict()
        
        params['country_code']=country_code

        params['phone_category_name']=phone_category_name

        
        if city_name is not None:
            params['city_name']=city_name

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetRegions', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_regulation_region_record(p)
            except TypeError as te:
                pass
        
        return res

    def add_push_credential(self, push_provider_name=None, push_provider_id=None, application_id=None, application_name=None, credential_bundle=None, cert_content=None, cert_file_name=None, cert_password=None, is_dev_mode=None, service_account_file=None, huawei_client_id=None, huawei_client_secret=None, huawei_application_id=None):
        """
        Adds push credentials.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if push_provider_name is not None:
            passed_args.append('push_provider_name')
        if push_provider_id is not None:
            passed_args.append('push_provider_id')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_push_credential")
        if len(passed_args) == 0:
            raise VoximplantException("None of push_provider_name, push_provider_id passed into add_push_credential")
        
        
        passed_args = []
        if cert_content is not None:
            passed_args.append('cert_content')
        if cert_file_name is not None:
            passed_args.append('cert_file_name')
        if cert_password is not None:
            passed_args.append('cert_password')
        if is_dev_mode is not None:
            passed_args.append('is_dev_mode')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_push_credential")
        if len(passed_args) == 0:
            raise VoximplantException("None of cert_content, cert_file_name, cert_password, is_dev_mode passed into add_push_credential")
        
        
        passed_args = []
        if service_account_file is not None:
            passed_args.append('service_account_file')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_push_credential")
        if len(passed_args) == 0:
            raise VoximplantException("None of service_account_file passed into add_push_credential")
        
        
        passed_args = []
        if huawei_client_id is not None:
            passed_args.append('huawei_client_id')
        if huawei_client_secret is not None:
            passed_args.append('huawei_client_secret')
        if huawei_application_id is not None:
            passed_args.append('huawei_application_id')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_push_credential")
        if len(passed_args) == 0:
            raise VoximplantException("None of huawei_client_id, huawei_client_secret, huawei_application_id passed into add_push_credential")
        
        
        
        if push_provider_name is not None:
            params['push_provider_name']=push_provider_name

        if push_provider_id is not None:
            params['push_provider_id']=push_provider_id

        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if credential_bundle is not None:
            params['credential_bundle']=credential_bundle

        if cert_content is not None:
            params['cert_content']=cert_content

        if cert_file_name is not None:
            params['cert_file_name']=cert_file_name

        if cert_password is not None:
            params['cert_password']=cert_password

        if is_dev_mode is not None:
            params['is_dev_mode']=is_dev_mode

        if service_account_file is not None:
            params['service_account_file']=service_account_file

        if huawei_client_id is not None:
            params['huawei_client_id']=huawei_client_id

        if huawei_client_secret is not None:
            params['huawei_client_secret']=huawei_client_secret

        if huawei_application_id is not None:
            params['huawei_application_id']=huawei_application_id

        
        res = self._perform_request('AddPushCredential', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_push_credential(self, push_credential_id, cert_content=None, cert_password=None, is_dev_mode=None, service_account_file=None, huawei_client_id=None, huawei_client_secret=None, huawei_application_id=None):
        """
        Modifies push credentials.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if cert_content is not None:
            passed_args.append('cert_content')
        if cert_password is not None:
            passed_args.append('cert_password')
        if is_dev_mode is not None:
            passed_args.append('is_dev_mode')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_push_credential")
        if len(passed_args) == 0:
            raise VoximplantException("None of cert_content, cert_password, is_dev_mode passed into set_push_credential")
        
        
        passed_args = []
        if service_account_file is not None:
            passed_args.append('service_account_file')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_push_credential")
        if len(passed_args) == 0:
            raise VoximplantException("None of service_account_file passed into set_push_credential")
        
        
        passed_args = []
        if huawei_client_id is not None:
            passed_args.append('huawei_client_id')
        if huawei_client_secret is not None:
            passed_args.append('huawei_client_secret')
        if huawei_application_id is not None:
            passed_args.append('huawei_application_id')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_push_credential")
        if len(passed_args) == 0:
            raise VoximplantException("None of huawei_client_id, huawei_client_secret, huawei_application_id passed into set_push_credential")
        
        
        params['push_credential_id']=push_credential_id

        
        if cert_content is not None:
            params['cert_content']=cert_content

        if cert_password is not None:
            params['cert_password']=cert_password

        if is_dev_mode is not None:
            params['is_dev_mode']=is_dev_mode

        if service_account_file is not None:
            params['service_account_file']=service_account_file

        if huawei_client_id is not None:
            params['huawei_client_id']=huawei_client_id

        if huawei_client_secret is not None:
            params['huawei_client_secret']=huawei_client_secret

        if huawei_application_id is not None:
            params['huawei_application_id']=huawei_application_id

        
        res = self._perform_request('SetPushCredential', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_push_credential(self, push_credential_id):
        """
        Removes push credentials.

        
        :rtype: dict
        """
        params = dict()
        
        params['push_credential_id']=push_credential_id

        
        
        res = self._perform_request('DelPushCredential', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_push_credential(self, push_credential_id=None, push_provider_name=None, push_provider_id=None, application_name=None, application_id=None, with_cert=None):
        """
        Gets push credentials.

        
        :rtype: dict
        """
        params = dict()
        
        
        if push_credential_id is not None:
            params['push_credential_id']=push_credential_id

        if push_provider_name is not None:
            params['push_provider_name']=push_provider_name

        if push_provider_id is not None:
            params['push_provider_id']=push_provider_id

        if application_name is not None:
            params['application_name']=application_name

        if application_id is not None:
            params['application_id']=application_id

        if with_cert is not None:
            params['with_cert']=with_cert

        
        res = self._perform_request('GetPushCredential', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_push_credential_info(p)
            except TypeError as te:
                pass
        
        return res

    def bind_push_credential(self, push_credential_id, application_id, bind=None):
        """
        Binds push credentials to applications.

        
        :rtype: dict
        """
        params = dict()
        
        params['push_credential_id']=self._serialize_list(push_credential_id)

        params['application_id']=self._serialize_list(application_id)

        
        if bind is not None:
            params['bind']=bind

        
        res = self._perform_request('BindPushCredential', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def add_dialogflow_key(self, application_id, json_credentials, application_name=None, description=None):
        """
        Adds a Dialogflow key.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['json_credentials']=json_credentials

        
        if application_name is not None:
            params['application_name']=application_name

        if description is not None:
            params['description']=description

        
        res = self._perform_request('AddDialogflowKey', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_dialogflow_key(self, dialogflow_key_id, description):
        """
        Edits a Dialogflow key.

        
        :rtype: dict
        """
        params = dict()
        
        params['dialogflow_key_id']=dialogflow_key_id

        params['description']=description

        
        
        res = self._perform_request('SetDialogflowKey', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_dialogflow_key(self, dialogflow_key_id):
        """
        Removes a Dialogflow key.

        
        :rtype: dict
        """
        params = dict()
        
        params['dialogflow_key_id']=dialogflow_key_id

        
        
        res = self._perform_request('DelDialogflowKey', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_dialogflow_keys(self, dialogflow_key_id=None, application_name=None, application_id=None):
        """
        Gets Dialogflow keys.

        
        :rtype: dict
        """
        params = dict()
        
        
        if dialogflow_key_id is not None:
            params['dialogflow_key_id']=dialogflow_key_id

        if application_name is not None:
            params['application_name']=application_name

        if application_id is not None:
            params['application_id']=application_id

        
        res = self._perform_request('GetDialogflowKeys', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_dialogflow_key_info(p)
            except TypeError as te:
                pass
        
        return res

    def bind_dialogflow_keys(self, dialogflow_key_id, application_id, bind=None):
        """
        Binds a Dialogflow key to the specified applications.

        
        :rtype: dict
        """
        params = dict()
        
        params['dialogflow_key_id']=dialogflow_key_id

        params['application_id']=self._serialize_list(application_id)

        
        if bind is not None:
            params['bind']=bind

        
        res = self._perform_request('BindDialogflowKeys', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def send_sms_message(self, source, destination, sms_body, store_body=None):
        """
        Sends an SMS message between two phone numbers. The source phone number should be purchased from Voximplant and support SMS (which is indicated by the <b>is_sms_supported</b> property in the objects returned by the [GetPhoneNumbers] Management API) and SMS should be enabled for it via the [ControlSms] Management API. SMS messages can be received via HTTP callbacks, see <a href='/docs/guides/managementapi/callbacks'>this article</a> for details.

        
        :rtype: dict
        """
        params = dict()
        
        params['source']=source

        params['destination']=destination

        params['sms_body']=sms_body

        
        if store_body is not None:
            params['store_body']=store_body

        
        res = self._perform_request('SendSmsMessage', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def a2p_send_sms(self, src_number, dst_numbers, text, store_body=None):
        """
        Sends an SMS message from the application to customers. The source phone number should be purchased from Voximplant and support SMS (which is indicated by the <b>is_sms_supported</b> property in the objects returned by the <a href='/docs/references/httpapi/managing_phone_numbers#getphonenumbers'>/GetPhoneNumbers</a> Management API) and SMS should be enabled for it via the <a href='/docs/references/httpapi/managing_sms#controlsms'>/ControlSms</a> Management API.

        
        :rtype: dict
        """
        params = dict()
        
        params['src_number']=src_number

        params['dst_numbers']=self._serialize_list(dst_numbers)

        params['text']=text

        
        if store_body is not None:
            params['store_body']=store_body

        
        res = self._perform_request('A2PSendSms', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_sms_transaction(p)
            except TypeError as te:
                pass
        
        return res

    def control_sms(self, phone_number, command):
        """
        Enables or disables sending and receiving SMS for the phone number. Can be used only for phone numbers with SMS support, which is indicated by the <b>is_sms_supported</b> property in the objects returned by the [GetPhoneNumbers] Management API. Each incoming SMS message is charged according to the <a href='//voximplant.com/pricing'>pricing</a>. If enabled, SMS can be sent from this phone number via the [SendSmsMessage] Management API and received via the [InboundSmsCallback] property of the HTTP callback. See <a href='/docs/guides/managementapi/callbacks'>this article</a> for HTTP callback details.

        
        :rtype: dict
        """
        params = dict()
        
        params['phone_number']=phone_number

        params['command']=command

        
        
        res = self._perform_request('ControlSms', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_record_storages(self, record_storage_id=None, record_storage_name=None):
        """
        Gets the record storages.

        
        :rtype: dict
        """
        params = dict()
        
        
        if record_storage_id is not None:
            params['record_storage_id']=self._serialize_list(record_storage_id)

        if record_storage_name is not None:
            params['record_storage_name']=self._serialize_list(record_storage_name)

        
        res = self._perform_request('GetRecordStorages', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_record_storage_info_type(res["result"])
        
        return res

    def create_key(self, description=None, key_name=None, role_id=None, role_name=None):
        """
        Creates a public/private key pair. You can optionally specify one or more roles for the key.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if role_id is not None:
            passed_args.append('role_id')
        if role_name is not None:
            passed_args.append('role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into create_key")
        
        
        
        if description is not None:
            params['description']=description

        if key_name is not None:
            params['key_name']=key_name

        if role_id is not None:
            params['role_id']=self._serialize_list(role_id)

        if role_name is not None:
            params['role_name']=self._serialize_list(role_name)

        
        res = self._perform_request('CreateKey', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_key_info(p)
            except TypeError as te:
                pass
        
        return res

    def get_keys(self, key_id=None, with_roles=None, offset=None, count=None):
        """
        Gets key info of the specified account.

        
        :rtype: dict
        """
        params = dict()
        
        
        if key_id is not None:
            params['key_id']=key_id

        if with_roles is not None:
            params['with_roles']=with_roles

        if offset is not None:
            params['offset']=offset

        if count is not None:
            params['count']=count

        
        res = self._perform_request('GetKeys', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_key_view(p)
            except TypeError as te:
                pass
        
        return res

    def update_key(self, key_id, description, key_name=None):
        """
        Updates info of the specified key.

        
        :rtype: dict
        """
        params = dict()
        
        params['key_id']=key_id

        params['description']=description

        
        if key_name is not None:
            params['key_name']=key_name

        
        res = self._perform_request('UpdateKey', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def delete_key(self, key_id):
        """
        Deletes the specified key.

        
        :rtype: dict
        """
        params = dict()
        
        params['key_id']=key_id

        
        
        res = self._perform_request('DeleteKey', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_key_roles(self, key_id, role_id=None, role_name=None):
        """
        Set roles for the specified key.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if role_id is not None:
            passed_args.append('role_id')
        if role_name is not None:
            passed_args.append('role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_key_roles")
        if len(passed_args) == 0:
            raise VoximplantException("None of role_id, role_name passed into set_key_roles")
        
        
        params['key_id']=key_id

        
        if role_id is not None:
            params['role_id']=self._serialize_list(role_id)

        if role_name is not None:
            params['role_name']=self._serialize_list(role_name)

        
        res = self._perform_request('SetKeyRoles', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_key_roles(self, key_id, with_expanded_roles=None):
        """
        Gets roles of the specified key.

        
        :rtype: dict
        """
        params = dict()
        
        params['key_id']=key_id

        
        if with_expanded_roles is not None:
            params['with_expanded_roles']=with_expanded_roles

        
        res = self._perform_request('GetKeyRoles', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_role_view(p)
            except TypeError as te:
                pass
        
        return res

    def remove_key_roles(self, key_id, role_id=None, role_name=None):
        """
        Removes the specified roles of a key.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if role_id is not None:
            passed_args.append('role_id')
        if role_name is not None:
            passed_args.append('role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into remove_key_roles")
        if len(passed_args) == 0:
            raise VoximplantException("None of role_id, role_name passed into remove_key_roles")
        
        
        params['key_id']=key_id

        
        if role_id is not None:
            params['role_id']=self._serialize_list(role_id)

        if role_name is not None:
            params['role_name']=self._serialize_list(role_name)

        
        res = self._perform_request('RemoveKeyRoles', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def add_sub_user(self, new_subuser_name, new_subuser_password, role_id=None, role_name=None, description=None):
        """
        Creates a subuser.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if role_id is not None:
            passed_args.append('role_id')
        if role_name is not None:
            passed_args.append('role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_sub_user")
        
        
        params['new_subuser_name']=new_subuser_name

        params['new_subuser_password']=new_subuser_password

        
        if role_id is not None:
            params['role_id']=self._serialize_list(role_id)

        if role_name is not None:
            params['role_name']=self._serialize_list(role_name)

        if description is not None:
            params['description']=description

        
        res = self._perform_request('AddSubUser', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_sub_user_id(res["result"])
        
        return res

    def get_sub_users(self, subuser_id=None, with_roles=None, offset=None, count=None):
        """
        Gets subusers.

        
        :rtype: dict
        """
        params = dict()
        
        
        if subuser_id is not None:
            params['subuser_id']=subuser_id

        if with_roles is not None:
            params['with_roles']=with_roles

        if offset is not None:
            params['offset']=offset

        if count is not None:
            params['count']=count

        
        res = self._perform_request('GetSubUsers', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_sub_user_view(p)
            except TypeError as te:
                pass
        
        return res

    def set_sub_user_info(self, subuser_id, old_subuser_password=None, new_subuser_password=None, description=None):
        """
        Edits a subuser.

        
        :rtype: dict
        """
        params = dict()
        
        params['subuser_id']=subuser_id

        
        if old_subuser_password is not None:
            params['old_subuser_password']=old_subuser_password

        if new_subuser_password is not None:
            params['new_subuser_password']=new_subuser_password

        if description is not None:
            params['description']=description

        
        res = self._perform_request('SetSubUserInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def del_sub_user(self, subuser_id):
        """
        Deletes a subuser.

        
        :rtype: dict
        """
        params = dict()
        
        params['subuser_id']=subuser_id

        
        
        res = self._perform_request('DelSubUser', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def set_sub_user_roles(self, subuser_id, role_id=None, role_name=None):
        """
        Adds the specified roles for a subuser.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if role_id is not None:
            passed_args.append('role_id')
        if role_name is not None:
            passed_args.append('role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_sub_user_roles")
        if len(passed_args) == 0:
            raise VoximplantException("None of role_id, role_name passed into set_sub_user_roles")
        
        
        params['subuser_id']=subuser_id

        
        if role_id is not None:
            params['role_id']=self._serialize_list(role_id)

        if role_name is not None:
            params['role_name']=self._serialize_list(role_name)

        
        res = self._perform_request('SetSubUserRoles', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_sub_user_roles(self, subuser_id, with_expanded_roles=None):
        """
        Gets the subuser's roles.

        
        :rtype: dict
        """
        params = dict()
        
        params['subuser_id']=subuser_id

        
        if with_expanded_roles is not None:
            params['with_expanded_roles']=with_expanded_roles

        
        res = self._perform_request('GetSubUserRoles', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_role_view(p)
            except TypeError as te:
                pass
        
        return res

    def remove_sub_user_roles(self, subuser_id, role_id=None, role_name=None, force=None):
        """
        Removes the specified roles of a subuser.

        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if role_id is not None:
            passed_args.append('role_id')
        if role_name is not None:
            passed_args.append('role_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into remove_sub_user_roles")
        if len(passed_args) == 0:
            raise VoximplantException("None of role_id, role_name passed into remove_sub_user_roles")
        
        
        params['subuser_id']=subuser_id

        
        if role_id is not None:
            params['role_id']=self._serialize_list(role_id)

        if role_name is not None:
            params['role_name']=self._serialize_list(role_name)

        if force is not None:
            params['force']=force

        
        res = self._perform_request('RemoveSubUserRoles', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_roles(self, group_name=None):
        """
        Gets all roles.

        
        :rtype: dict
        """
        params = dict()
        
        
        if group_name is not None:
            params['group_name']=group_name

        
        res = self._perform_request('GetRoles', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_role_view(p)
            except TypeError as te:
                pass
        
        return res

    def get_role_groups(self):
        """
        Gets role groups.

        
        :rtype: dict
        """
        params = dict()
        
        
        
        res = self._perform_request('GetRoleGroups', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_role_group_view(p)
            except TypeError as te:
                pass
        
        return res

    def set_key_value_item(self, key, value, application_id, application_name=None, ttl=None, expires_at=None):
        """
        Creates or updates a key-value pair. If an existing key is passed, the method returns the existing item and changes the value if needed. The keys should be unique within a Voximplant application.

        
        :rtype: dict
        """
        params = dict()
        
        params['key']=key

        params['value']=value

        params['application_id']=application_id

        
        if application_name is not None:
            params['application_name']=application_name

        if ttl is not None:
            params['ttl']=ttl

        if expires_at is not None:
            params['expires_at']=expires_at

        
        res = self._perform_request('SetKeyValueItem', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_key_value_items(res["result"])
        
        return res

    def del_key_value_item(self, key, application_id, application_name=None):
        """
        Deletes the specified key-value pair from the storage.

        
        :rtype: dict
        """
        params = dict()
        
        params['key']=key

        params['application_id']=application_id

        
        if application_name is not None:
            params['application_name']=application_name

        
        res = self._perform_request('DelKeyValueItem', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def get_key_value_item(self, key, application_id, application_name=None):
        """
        Gets the specified key-value pair from the storage.

        
        :rtype: dict
        """
        params = dict()
        
        params['key']=key

        params['application_id']=application_id

        
        if application_name is not None:
            params['application_name']=application_name

        
        res = self._perform_request('GetKeyValueItem', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_key_value_items(res["result"])
        
        return res

    def get_key_value_items(self, key, application_id, count=None, offset=None, application_name=None):
        """
        Gets all the key-value pairs in which the keys begin with a pattern.

        
        :rtype: dict
        """
        params = dict()
        
        params['key']=key

        params['application_id']=application_id

        
        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if application_name is not None:
            params['application_name']=application_name

        
        res = self._perform_request('GetKeyValueItems', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_key_value_items(res["result"])
        
        return res

    def get_key_value_keys(self, application_id, key=None, count=None, offset=None, application_name=None):
        """
        Gets all the keys of key-value pairs.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        
        if key is not None:
            params['key']=key

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if application_name is not None:
            params['application_name']=application_name

        
        res = self._perform_request('GetKeyValueKeys', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_key_value_keys(res["result"])
        
        return res

    def get_account_invoices(self, count=None, offset=None):
        """
        Gets all invoices of the specified USD or EUR account.

        
        :rtype: dict
        """
        params = dict()
        
        
        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('GetAccountInvoices', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_account_invoice(res["result"])
        
        return res

    def get_sms_history(self, source_number=None, destination_number=None, direction=None, count=None, offset=None, from_date=None, to_date=None, output=None):
        """
        Gets the history of sent and/or received SMS.

        
        :rtype: dict
        """
        params = dict()
        
        
        if source_number is not None:
            params['source_number']=source_number

        if destination_number is not None:
            params['destination_number']=destination_number

        if direction is not None:
            params['direction']=direction

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if from_date is not None:
            params['from_date']=self._py_datetime_to_api(from_date)

        if to_date is not None:
            params['to_date']=self._py_datetime_to_api(to_date)

        if output is not None:
            params['output']=output

        
        res = self._perform_request('GetSmsHistory', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_sms_history_type(p)
            except TypeError as te:
                pass
        
        return res

    def a2p_get_sms_history(self, source_number=None, destination_number=None, count=None, offset=None, from_date=None, to_date=None, output=None, delivery_status=None):
        """
        Gets the history of sent/or received A2P SMS.

        
        :rtype: dict
        """
        params = dict()
        
        
        if source_number is not None:
            params['source_number']=source_number

        if destination_number is not None:
            params['destination_number']=destination_number

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if from_date is not None:
            params['from_date']=self._py_datetime_to_api(from_date)

        if to_date is not None:
            params['to_date']=self._py_datetime_to_api(to_date)

        if output is not None:
            params['output']=output

        if delivery_status is not None:
            params['delivery_status']=delivery_status

        
        res = self._perform_request('A2PGetSmsHistory', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            try:
                for p in res["result"]:
                    self._preprocess_a2p_sms_history_type(p)
            except TypeError as te:
                pass
        
        return res

    def sq__add_queue(self, application_id, sq_queue_name, call_agent_selection, call_task_selection, application_name=None, im_agent_selection=None, im_task_selection=None, description=None, call_max_waiting_time=None, im_max_waiting_time=None, call_max_queue_size=None, im_max_queue_size=None, priority=None):
        """
        Adds a new queue.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['sq_queue_name']=sq_queue_name

        params['call_agent_selection']=call_agent_selection

        params['call_task_selection']=call_task_selection

        
        if application_name is not None:
            params['application_name']=application_name

        if im_agent_selection is not None:
            params['im_agent_selection']=im_agent_selection

        if im_task_selection is not None:
            params['im_task_selection']=im_task_selection

        if description is not None:
            params['description']=description

        if call_max_waiting_time is not None:
            params['call_max_waiting_time']=call_max_waiting_time

        if im_max_waiting_time is not None:
            params['im_max_waiting_time']=im_max_waiting_time

        if call_max_queue_size is not None:
            params['call_max_queue_size']=call_max_queue_size

        if im_max_queue_size is not None:
            params['im_max_queue_size']=im_max_queue_size

        if priority is not None:
            params['priority']=priority

        
        res = self._perform_request('SQ_AddQueue', params)
        
        return res

    def sq__set_queue_info(self, application_id, sq_queue_id, application_name=None, sq_queue_name=None, new_sq_queue_name=None, call_agent_selection=None, im_agent_selection=None, call_task_selection=None, im_task_selection=None, description=None, call_max_waiting_time=None, im_max_waiting_time=None, call_max_queue_size=None, im_max_queue_size=None, priority=None):
        """
        Edits an existing queue.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['sq_queue_id']=sq_queue_id

        
        if application_name is not None:
            params['application_name']=application_name

        if sq_queue_name is not None:
            params['sq_queue_name']=sq_queue_name

        if new_sq_queue_name is not None:
            params['new_sq_queue_name']=new_sq_queue_name

        if call_agent_selection is not None:
            params['call_agent_selection']=call_agent_selection

        if im_agent_selection is not None:
            params['im_agent_selection']=im_agent_selection

        if call_task_selection is not None:
            params['call_task_selection']=call_task_selection

        if im_task_selection is not None:
            params['im_task_selection']=im_task_selection

        if description is not None:
            params['description']=description

        if call_max_waiting_time is not None:
            params['call_max_waiting_time']=call_max_waiting_time

        if im_max_waiting_time is not None:
            params['im_max_waiting_time']=im_max_waiting_time

        if call_max_queue_size is not None:
            params['call_max_queue_size']=call_max_queue_size

        if im_max_queue_size is not None:
            params['im_max_queue_size']=im_max_queue_size

        if priority is not None:
            params['priority']=priority

        
        res = self._perform_request('SQ_SetQueueInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def sq__del_queue(self, application_id, sq_queue_id, application_name=None, sq_queue_name=None):
        """
        Deletes a queue.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['sq_queue_id']=self._serialize_list(sq_queue_id)

        
        if application_name is not None:
            params['application_name']=application_name

        if sq_queue_name is not None:
            params['sq_queue_name']=self._serialize_list(sq_queue_name)

        
        res = self._perform_request('SQ_DelQueue', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def sq__get_queues(self, application_id, application_name=None, sq_queue_id=None, sq_queue_name=None, sq_queue_name_template=None, user_id=None, user_name=None, excluded_user_id=None, excluded_user_name=None, count=None, offset=None, with_agentcount=None):
        """
        Gets the queue(s).

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        
        if application_name is not None:
            params['application_name']=application_name

        if sq_queue_id is not None:
            params['sq_queue_id']=self._serialize_list(sq_queue_id)

        if sq_queue_name is not None:
            params['sq_queue_name']=self._serialize_list(sq_queue_name)

        if sq_queue_name_template is not None:
            params['sq_queue_name_template']=sq_queue_name_template

        if user_id is not None:
            params['user_id']=user_id

        if user_name is not None:
            params['user_name']=user_name

        if excluded_user_id is not None:
            params['excluded_user_id']=excluded_user_id

        if excluded_user_name is not None:
            params['excluded_user_name']=excluded_user_name

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        if with_agentcount is not None:
            params['with_agentcount']=with_agentcount

        
        res = self._perform_request('SQ_GetQueues', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_get_sq_queues_result(res["result"])
        
        return res

    def sq__add_skill(self, application_id, sq_skill_name, application_name=None, description=None):
        """
        Adds a new skill to the app.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['sq_skill_name']=sq_skill_name

        
        if application_name is not None:
            params['application_name']=application_name

        if description is not None:
            params['description']=description

        
        res = self._perform_request('SQ_AddSkill', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def sq__del_skill(self, application_id, sq_skill_id, application_name=None, sq_skill_name=None):
        """
        Deletes a skill and detaches it from agents.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['sq_skill_id']=self._serialize_list(sq_skill_id)

        
        if application_name is not None:
            params['application_name']=application_name

        if sq_skill_name is not None:
            params['sq_skill_name']=self._serialize_list(sq_skill_name)

        
        res = self._perform_request('SQ_DelSkill', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def sq__set_skill_info(self, application_id, sq_skill_id, application_name=None, sq_skill_name=None, new_sq_skill_name=None, description=None):
        """
        Edits an existing skill.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['sq_skill_id']=sq_skill_id

        
        if application_name is not None:
            params['application_name']=application_name

        if sq_skill_name is not None:
            params['sq_skill_name']=sq_skill_name

        if new_sq_skill_name is not None:
            params['new_sq_skill_name']=new_sq_skill_name

        if description is not None:
            params['description']=description

        
        res = self._perform_request('SQ_SetSkillInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def sq__bind_skill(self, application_id, user_id, sq_skills, application_name=None, user_name=None, bind_mode=None):
        """
        Binds skills to agents.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['user_id']=self._serialize_list(user_id)

        params['sq_skills']=sq_skills

        
        if application_name is not None:
            params['application_name']=application_name

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if bind_mode is not None:
            params['bind_mode']=bind_mode

        
        res = self._perform_request('SQ_BindSkill', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def sq__unbind_skill(self, application_id, user_id, sq_skill_id, application_name=None, user_name=None, sq_skill_name=None):
        """
        Unbinds skills from agents.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['user_id']=self._serialize_list(user_id)

        params['sq_skill_id']=self._serialize_list(sq_skill_id)

        
        if application_name is not None:
            params['application_name']=application_name

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if sq_skill_name is not None:
            params['sq_skill_name']=self._serialize_list(sq_skill_name)

        
        res = self._perform_request('SQ_UnbindSkill', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def sq__get_skills(self, application_id, application_name=None, user_id=None, user_name=None, sq_skill_id=None, sq_skill_name=None, sq_skill_name_template=None, excluded_user_id=None, excluded_user_name=None, count=None, offset=None):
        """
        Gets the skill(s).

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        
        if application_name is not None:
            params['application_name']=application_name

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if sq_skill_id is not None:
            params['sq_skill_id']=self._serialize_list(sq_skill_id)

        if sq_skill_name is not None:
            params['sq_skill_name']=self._serialize_list(sq_skill_name)

        if sq_skill_name_template is not None:
            params['sq_skill_name_template']=sq_skill_name_template

        if excluded_user_id is not None:
            params['excluded_user_id']=excluded_user_id

        if excluded_user_name is not None:
            params['excluded_user_name']=excluded_user_name

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('SQ_GetSkills', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_get_sq_skills_result(res["result"])
        
        return res

    def sq__bind_agent(self, application_id, sq_queue_id, user_id, application_name=None, sq_queue_name=None, user_name=None, bind_mode=None):
        """
        Binds agents to a queue.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['sq_queue_id']=sq_queue_id

        params['user_id']=self._serialize_list(user_id)

        
        if application_name is not None:
            params['application_name']=application_name

        if sq_queue_name is not None:
            params['sq_queue_name']=sq_queue_name

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if bind_mode is not None:
            params['bind_mode']=bind_mode

        
        res = self._perform_request('SQ_BindAgent', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def sq__unbind_agent(self, application_id, sq_queue_id, user_id, application_name=None, sq_queue_name=None, user_name=None):
        """
        Unbinds agents from queues.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['sq_queue_id']=self._serialize_list(sq_queue_id)

        params['user_id']=self._serialize_list(user_id)

        
        if application_name is not None:
            params['application_name']=application_name

        if sq_queue_name is not None:
            params['sq_queue_name']=self._serialize_list(sq_queue_name)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        
        res = self._perform_request('SQ_UnbindAgent', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res

    def sq__get_agents(self, application_id, handle_calls, application_name=None, sq_queue_id=None, sq_queue_name=None, excluded_sq_queue_id=None, excluded_sq_queue_name=None, sq_skills=None, user_id=None, user_name=None, user_name_template=None, sq_statuses=None, with_sq_skills=None, with_sq_queues=None, with_sq_statuses=None, count=None, offset=None):
        """
        Gets agents.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['handle_calls']=handle_calls

        
        if application_name is not None:
            params['application_name']=application_name

        if sq_queue_id is not None:
            params['sq_queue_id']=self._serialize_list(sq_queue_id)

        if sq_queue_name is not None:
            params['sq_queue_name']=self._serialize_list(sq_queue_name)

        if excluded_sq_queue_id is not None:
            params['excluded_sq_queue_id']=excluded_sq_queue_id

        if excluded_sq_queue_name is not None:
            params['excluded_sq_queue_name']=excluded_sq_queue_name

        if sq_skills is not None:
            params['sq_skills']=sq_skills

        if user_id is not None:
            params['user_id']=self._serialize_list(user_id)

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if user_name_template is not None:
            params['user_name_template']=user_name_template

        if sq_statuses is not None:
            params['sq_statuses']=sq_statuses

        if with_sq_skills is not None:
            params['with_sq_skills']=with_sq_skills

        if with_sq_queues is not None:
            params['with_sq_queues']=with_sq_queues

        if with_sq_statuses is not None:
            params['with_sq_statuses']=with_sq_statuses

        if count is not None:
            params['count']=count

        if offset is not None:
            params['offset']=offset

        
        res = self._perform_request('SQ_GetAgents', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        if "result" in res:
            self._preprocess_get_sq_agents_result(res["result"])
        
        return res

    def sq__set_agent_info(self, application_id, user_id, handle_calls, application_name=None, user_name=None, max_simultaneous_conversations=None):
        """
        Edits the agent settings.

        
        :rtype: dict
        """
        params = dict()
        
        params['application_id']=application_id

        params['user_id']=self._serialize_list(user_id)

        params['handle_calls']=handle_calls

        
        if application_name is not None:
            params['application_name']=application_name

        if user_name is not None:
            params['user_name']=self._serialize_list(user_name)

        if max_simultaneous_conversations is not None:
            params['max_simultaneous_conversations']=max_simultaneous_conversations

        
        res = self._perform_request('SQ_SetAgentInfo', params)
        
        if "error" in res:
            raise VoximplantException(res["error"]["msg"], res["error"]["code"])
        
        
        return res