import json
import os
import datetime
import pytz
import requests
import jwt
import time
import sys

class VoximplantException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class VoximplantAPI:
    """Voximplant API access helper"""

    def _api_date_to_py(self, d):
        return datetime.datetime.strptime(d, "%Y-%m-%d").date()

    def _api_datetime_utc_to_py(self, d):
        return datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.utc)

    def _py_datetime_to_api(self, d):
        if d.tzinfo is None:
            return d.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return d.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")

    def build_auth_header(self):
        ts = int(time.time())
        token = jwt.encode({"iss":self.account_id, "iat":ts-5, "exp":ts+24}, self.credentials["private_key"], algorithm='RS256', headers={"kid": self.credentials["key_id"]})
        if sys.version_info[0] < 3:
            return 'Bearer '+token
        else:
            return 'Bearer '+token.decode("utf-8")


    def _perform_request(self, cmd, args):
        params = args.copy()
        params["cmd"] = cmd
        headers={'Authorization': self.build_auth_header()}
        result = requests.post("https://{}/platform_api".format(self.endpoint), params=params, headers=headers)
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
            for k in s["billing_limits"]:
                self._preprocess_billing_limits_type(k)

    def _preprocess_billing_limits_type(self, s):
        if "robokassa" in s:
            for k in s["robokassa"]:
                self._preprocess_billing_limit_info_type(k)
        if "bank_card" in s:
            for k in s["bank_card"]:
                self._preprocess_billing_limit_info_type(k)
        if "invoice" in s:
            for k in s["invoice"]:
                self._preprocess_billing_limit_info_type(k)

    def _preprocess_billing_limit_info_type(self, s):
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
        if "package" in s:
            for k in s["package"]:
                self._preprocess_plan_package_type(k)

    def _preprocess_plan_package_type(self, s):
            pass

    def _preprocess_application_info_type(self, s):
        if "modified" in s:
            s["modified"] = self._api_datetime_utc_to_py(s["modified"])
        if "users" in s:
            for k in s["users"]:
                self._preprocess_user_info_type(k)

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
            s["store_until"] = self._api_datetime_utc_to_py(s["store_until"])
        if "error" in s:
            self._preprocess_api__error(s["error"])

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
            pass

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
        if "transcription_complete" in s:
            self._preprocess_transcription_complete_callback(s["transcription_complete"])
        if "sms_inbound" in s:
            self._preprocess_inbound_sms_callback(s["sms_inbound"])
        if "new_invoice" in s:
            self._preprocess_new_invoice_callback(s["new_invoice"])

    def _preprocess_account_document_uploaded_callback(self, s):
        if "uploaded" in s:
            s["uploaded"] = self._api_datetime_utc_to_py(s["uploaded"])

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

    def _preprocess_reset_account_password_request_callback(self, s):
            pass

    def _preprocess_sip_registration_fail_callback(self, s):
            pass

    def _preprocess_subscription_is_detached_callback(self, s):
        if "subscriptions" in s:
            for k in s["subscriptions"]:
                self._preprocess_subscription_is_detached_callback_item(k)

    def _preprocess_subscription_is_detached_callback_item(self, s):
            pass

    def _preprocess_subscription_is_frozen_callback(self, s):
        if "subscriptions" in s:
            for k in s["subscriptions"]:
                self._preprocess_subscription_is_frozen_callback_item(k)

    def _preprocess_subscription_is_frozen_callback_item(self, s):
            pass

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
            pass

    def _preprocess_expiring_caller_id_callback(self, s):
        if "expiration_date" in s:
            s["expiration_date"] = self._api_date_to_py(s["expiration_date"])

    def _preprocess_transcription_complete_callback(self, s):
        if "transcription_complete" in s:
            self._preprocess_transcription_complete_callback_item(s["transcription_complete"])

    def _preprocess_transcription_complete_callback_item(self, s):
            pass

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
            self._preprocess_push_credential_content(s["content"])
        if "applications" in s:
            for k in s["applications"]:
                self._preprocess_application_info_type(k)

    def _preprocess_push_credential_content(self, s):
            pass

    def _preprocess_inbound_sms_callback(self, s):
        if "sms_inbound" in s:
            for k in s["sms_inbound"]:
                self._preprocess_inbound_sms_callback_item(k)

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


    def get_account_info(self, return_live_balance=None):
        """
        Gets the account's info such as account_id, account_name, account_email etc.

        
        :param return_live_balance: Set true to get the account's live balance. 
        :type return_live_balance: bool
        
        :rtype: dict
        """
        params = dict()
        
        
        if return_live_balance is not None:
            params['return_live_balance']=return_live_balance

        
        res = self._perform_request('GetAccountInfo', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
                self._preprocess_account_info_type(res["result"])
        return res

    def set_account_info(self, new_account_email=None, new_account_password=None, language_code=None, location=None, account_first_name=None, account_last_name=None, mobile_phone=None, min_balance_to_notify=None, account_notifications=None, tariff_changing_notifications=None, news_notifications=None, send_js_error=None, billing_address_name=None, billing_address_country_code=None, billing_address_address=None, billing_address_zip=None, billing_address_phone=None, account_custom_data=None, callback_url=None, callback_salt=None):
        """
        Edits the account's profile.

        
        :param new_account_email:  
        :type new_account_email: str
        
        :param new_account_password: The password length must be at least 6 symbols. 
        :type new_account_password: str
        
        :param language_code: The notification language code (2 symbols, ISO639-1). The following values are available: aa (Afar), ab (Abkhazian), af (Afrikaans), am (Amharic), ar (Arabic), as (Assamese), ay (Aymara), az (Azerbaijani), ba (Bashkir), be (Belarusian), bg (Bulgarian), bh (Bihari), bi (Bislama), bn (Bengali), bo (Tibetan), br (Breton), ca (Catalan), co (Corsican), cs (Czech), cy (Welch), da (Danish), de (German), dz (Bhutani), el (Greek), en (English), eo (Esperanto), es (Spanish), et (Estonian), eu (Basque), fa (Persian), fi (Finnish), fj (Fiji), fo (Faeroese), fr (French), fy (Frisian), ga (Irish), gd (Scots Gaelic), gl (Galician), gn (Guarani), gu (Gujarati), ha (Hausa), hi (Hindi), he (Hebrew), hr (Croatian), hu (Hungarian), hy (Armenian), ia (Interlingua), id (Indonesian), ie (Interlingue), ik (Inupiak), in (Indonesian), is (Icelandic), it (Italian), iu (Inuktitut), iw (Hebrew), ja (Japanese), ji (Yiddish), jw (Javanese), ka (Georgian), kk (Kazakh), kl (Greenlandic), km (Cambodian), kn (Kannada), ko (Korean), ks (Kashmiri), ku (Kurdish), ky (Kirghiz), la (Latin), ln (Lingala), lo (Laothian), lt (Lithuanian), lv (Latvian), mg (Malagasy), mi (Maori), mk (Macedonian), ml (Malayalam), mn (Mongolian), mo (Moldavian), mr (Marathi), ms (Malay), mt (Maltese), my (Burmese), na (Nauru), ne (Nepali), nl (Dutch), no (Norwegian), oc (Occitan), om (Oromo), or (Oriya), pa (Punjabi), pl (Polish), ps (Pashto), pt (Portuguese), qu (Quechua), rm (Rhaeto-Romance), rn (Kirundi), ro (Romanian), ru (Russian), rw (Kinyarwanda), sa (Sanskrit), sd (Sindhi), sg (Sangro), sh (Serbo-Croatian), si (Singhalese), sk (Slovak), sl (Slovenian), sm (Samoan), sn (Shona), so (Somali), sq (Albanian), sr (Serbian), ss (Siswati), st (Sesotho), su (Sudanese), sv (Swedish), sw (Swahili), ta (Tamil), te (Tegulu), tg (Tajik), th (Thai), ti (Tigrinya), tk (Turkmen), tl (Tagalog), tn (Setswana), to (Tonga), tr (Turkish), ts (Tsonga), tt (Tatar), tw (Twi), ug (Uigur), uk (Ukrainian), ur (Urdu), uz (Uzbek), vi (Vietnamese), vo (Volapuk), wo (Wolof), xh (Xhosa), yi (Yiddish), yo (Yoruba), za (Zhuang), zh (Chinese), zu (Zulu) 
        :type language_code: str
        
        :param location: The account location (timezone). Examples: America/Los_Angeles, GMT-8, GMT-08:00, GMT+10 
        :type location: str
        
        :param account_first_name: The first name. 
        :type account_first_name: str
        
        :param account_last_name: The last name. 
        :type account_last_name: str
        
        :param mobile_phone: The mobile phone linked to the account. 
        :type mobile_phone: str
        
        :param min_balance_to_notify: The min balance value to notify by email or SMS. 
        :type min_balance_to_notify: decimal
        
        :param account_notifications: Are the VoxImplant notifications required? 
        :type account_notifications: bool
        
        :param tariff_changing_notifications: Set to true to receive the emails about the VoxImplant plan changing. 
        :type tariff_changing_notifications: bool
        
        :param news_notifications: Set to true to receive the emails about the VoxImplant news. 
        :type news_notifications: bool
        
        :param send_js_error: Set to true to receive the emails about a JS scenario error. 
        :type send_js_error: bool
        
        :param billing_address_name: The company or businessman name. 
        :type billing_address_name: str
        
        :param billing_address_country_code: The billing address country code (2 symbols, ISO 3166-1 alpha-2). The following values are available: AF (Afghanistan), AL (Albania), DZ (Algeria), AS (American Samoa), AD (Andorra), AO (Angola), AI (Anguilla), AQ (Antarctica), AG (Antigua and Barbuda), AR (Argentina), AM (Armenia), AW (Aruba), AU (Australia), AT (Austria), AZ (Azerbaijan), BH (Bahrain), BD (Bangladesh), BB (Barbados), BY (Belarus), BE (Belgium), BZ (Belize), BJ (Benin), BM (Bermuda), BT (Bhutan), BO (Bolivia), BA (Bosnia and Herzegovina), BW (Botswana), BV (Bouvet Island), BR (Brazil), IO (British Indian Ocean Territory), BN (Brunei), BG (Bulgaria), BF (Burkina Faso), BI (Burundi), KH (Cambodia), CM (Cameroon), CA (Canada), CV (Cape Verde), KY (Cayman Islands), CF (Central African Republic), TD (Chad), CL (Chile), CN (China), CX (Christmas Island), CO (Colombia), KM (Comoros), CG (Congo), CK (Cook Islands), CR (Costa Rica), HR (Croatia), CU (Cuba), CY (Cyprus), CZ (Czech Republic), DK (Denmark), DJ (Djibouti), DM (Dominica), DO (Dominican Republic), EC (Ecuador), EG (Egypt), SV (El Salvador), GQ (Equatorial Guinea), ER (Eritrea), EE (Estonia), ET (Ethiopia), FO (Faroe Islands), FJ (Fiji Islands), FI (Finland), FR (France), GF (French Guiana), PF (French Polynesia), TF (French Southern and Antarctic Lands), GA (Gabon), GE (Georgia), DE (Germany), GH (Ghana), GI (Gibraltar), GR (Greece), GL (Greenland), GD (Grenada), GP (Guadeloupe), GU (Guam), GT (Guatemala), GG (Guernsey), GN (Guinea), GY (Guyana), HT (Haiti), HM (Heard Island and McDonald Islands), HN (Honduras), HU (Hungary), IS (Iceland), IN (India), ID (Indonesia), IR (Iran), IQ (Iraq), IE (Ireland), IL (Israel), IT (Italy), JM (Jamaica), JP (Japan), JE (Jersey), JO (Jordan), KZ (Kazakhstan), KE (Kenya), KI (Kiribati), KR (Korea), KW (Kuwait), KG (Kyrgyzstan), LA (Laos), LV (Latvia), LB (Lebanon), LS (Lesotho), LR (Liberia), LY (Libya), LI (Liechtenstein), LT (Lithuania), LU (Luxembourg), MG (Madagascar), MW (Malawi), MY (Malaysia), MV (Maldives), ML (Mali), MT (Malta), MH (Marshall Islands), MQ (Martinique), MR (Mauritania), MU (Mauritius), YT (Mayotte), MX (Mexico), FM (Micronesia), MD (Moldova), MC (Monaco), MN (Mongolia), ME (Montenegro), MS (Montserrat), MA (Morocco), MZ (Mozambique), MM (Myanmar), NA (Namibia), NR (Nauru), NP (Nepal), NL (Netherlands), AN (Netherlands Antilles), NC (New Caledonia), NZ (New Zealand), NI (Nicaragua), NE (Niger), NG (Nigeria), NU (Niue), NF (Norfolk Island), KP (North Korea), MP (Northern Mariana Islands), NO (Norway), OM (Oman), PK (Pakistan), PW (Palau), PS (Palestinian Authority), PA (Panama), PG (Papua New Guinea), PY (Paraguay), PE (Peru), PH (Philippines), PN (Pitcairn Islands), PL (Poland), PT (Portugal), PR (Puerto Rico), QA (Qatar), RE (Reunion), RO (Romania), RU (Russia), RW (Rwanda), WS (Samoa), SM (San Marino), SA (Saudi Arabia), SN (Senegal), RS (Serbia), SC (Seychelles), SL (Sierra Leone), SG (Singapore), SK (Slovakia), SI (Slovenia), SB (Solomon Islands), SO (Somalia), ZA (South Africa), GS (South Georgia and the South Sandwich Islands), ES (Spain), LK (Sri Lanka), SD (Sudan), SR (Suriname), SZ (Swaziland), SE (Sweden), CH (Switzerland), SY (Syria), ST (Sao Tome and Principe), TW (Taiwan), TJ (Tajikistan), TZ (Tanzania), TH (Thailand), TG (Togo), TK (Tokelau), TO (Tonga), TT (Trinidad and Tobago), TN (Tunisia), TR (Turkey), TM (Turkmenistan), TC (Turks and Caicos Islands), TV (Tuvalu), UG (Uganda), UA (Ukraine), AE (United Arab Emirates), GB (United Kingdom), US (United States), UY (Uruguay), UZ (Uzbekistan), VU (Vanuatu), VA (Vatican City), VE (Venezuela), VN (Vietnam), VI (Virgin Islands), WF (Wallis and Futuna), EH (Western Sahara), YE (Yemen), ZM (Zambia), ZW (Zimbabwe), AX (Aland Islands) 
        :type billing_address_country_code: str
        
        :param billing_address_address: The office address. 
        :type billing_address_address: str
        
        :param billing_address_zip: The office ZIP. 
        :type billing_address_zip: str
        
        :param billing_address_phone: The office phone number. 
        :type billing_address_phone: str
        
        :param account_custom_data: The custom data. 
        :type account_custom_data: str
        
        :param callback_url: If URL is specified, Voximplant cloud will make HTTP POST requests to it when something happens. For a full list of reasons see the <b>type</b> field of the [AccountCallback] structure. The HTTP request will have a JSON-encoded body that conforms to the [AccountCallbacks] structure 
        :type callback_url: str
        
        :param callback_salt: If salt string is specified, each HTTP request made by the Voximplant cloud toward the <b>callback_url</b> will have a <b>salt</b> field set to MD5 hash of account information and salt. That hash can be used be a developer to ensure that HTTP request is made by the Voximplant cloud 
        :type callback_salt: str
        
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

        if mobile_phone is not None:
            params['mobile_phone']=mobile_phone

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

        
        res = self._perform_request('SetAccountInfo', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_child_account_info(self, child_account_id=None, child_account_name=None, child_account_email=None, new_child_account_email=None, new_child_account_password=None, account_notifications=None, tariff_changing_notifications=None, news_notifications=None, active=None, language_code=None, location=None, min_balance_to_notify=None, support_robokassa=None, support_bank_card=None, support_invoice=None, can_use_restricted=None, min_payment_amount=None):
        """
        Edits the account's profile.

        
        :param child_account_id: The child account ID list or the 'all' value. 
        :type child_account_id: list | int | string
        
        :param child_account_name: The child account name list. Can be used instead of <b>child_account_id</b>. 
        :type child_account_name: list | string
        
        :param child_account_email: The child account email list. Can be used instead of <b>child_account_id</b>. 
        :type child_account_email: list | string
        
        :param new_child_account_email: The new child account email. 
        :type new_child_account_email: str
        
        :param new_child_account_password: The new child account password. 
        :type new_child_account_password: str
        
        :param account_notifications: Are the VoxImplant notifications required? 
        :type account_notifications: bool
        
        :param tariff_changing_notifications: Set to true to receive the emails about the VoxImplant plan changing. 
        :type tariff_changing_notifications: bool
        
        :param news_notifications: Set to true to receive the emails about the VoxImplant news. 
        :type news_notifications: bool
        
        :param active: Set false to disable the child account. 
        :type active: bool
        
        :param language_code: The notification language code (2 symbols, ISO639-1). The following values are available: aa (Afar), ab (Abkhazian), af (Afrikaans), am (Amharic), ar (Arabic), as (Assamese), ay (Aymara), az (Azerbaijani), ba (Bashkir), be (Belarusian), bg (Bulgarian), bh (Bihari), bi (Bislama), bn (Bengali), bo (Tibetan), br (Breton), ca (Catalan), co (Corsican), cs (Czech), cy (Welch), da (Danish), de (German), dz (Bhutani), el (Greek), en (English), eo (Esperanto), es (Spanish), et (Estonian), eu (Basque), fa (Persian), fi (Finnish), fj (Fiji), fo (Faeroese), fr (French), fy (Frisian), ga (Irish), gd (Scots Gaelic), gl (Galician), gn (Guarani), gu (Gujarati), ha (Hausa), hi (Hindi), he (Hebrew), hr (Croatian), hu (Hungarian), hy (Armenian), ia (Interlingua), id (Indonesian), ie (Interlingue), ik (Inupiak), in (Indonesian), is (Icelandic), it (Italian), iu (Inuktitut), iw (Hebrew), ja (Japanese), ji (Yiddish), jw (Javanese), ka (Georgian), kk (Kazakh), kl (Greenlandic), km (Cambodian), kn (Kannada), ko (Korean), ks (Kashmiri), ku (Kurdish), ky (Kirghiz), la (Latin), ln (Lingala), lo (Laothian), lt (Lithuanian), lv (Latvian), mg (Malagasy), mi (Maori), mk (Macedonian), ml (Malayalam), mn (Mongolian), mo (Moldavian), mr (Marathi), ms (Malay), mt (Maltese), my (Burmese), na (Nauru), ne (Nepali), nl (Dutch), no (Norwegian), oc (Occitan), om (Oromo), or (Oriya), pa (Punjabi), pl (Polish), ps (Pashto), pt (Portuguese), qu (Quechua), rm (Rhaeto-Romance), rn (Kirundi), ro (Romanian), ru (Russian), rw (Kinyarwanda), sa (Sanskrit), sd (Sindhi), sg (Sangro), sh (Serbo-Croatian), si (Singhalese), sk (Slovak), sl (Slovenian), sm (Samoan), sn (Shona), so (Somali), sq (Albanian), sr (Serbian), ss (Siswati), st (Sesotho), su (Sudanese), sv (Swedish), sw (Swahili), ta (Tamil), te (Tegulu), tg (Tajik), th (Thai), ti (Tigrinya), tk (Turkmen), tl (Tagalog), tn (Setswana), to (Tonga), tr (Turkish), ts (Tsonga), tt (Tatar), tw (Twi), ug (Uigur), uk (Ukrainian), ur (Urdu), uz (Uzbek), vi (Vietnamese), vo (Volapuk), wo (Wolof), xh (Xhosa), yi (Yiddish), yo (Yoruba), za (Zhuang), zh (Chinese), zu (Zulu) 
        :type language_code: str
        
        :param location: The child account location (timezone). Examples: America/Los_Angeles, GMT-8, GMT-08:00, GMT+10 
        :type location: str
        
        :param min_balance_to_notify: The min balance value to notify by email or SMS. 
        :type min_balance_to_notify: decimal
        
        :param support_robokassa: Set to true to allow the robokassa payments. 
        :type support_robokassa: bool
        
        :param support_bank_card: Set to true to allow the bank card payments. 
        :type support_bank_card: bool
        
        :param support_invoice: Set to true to allow the bank invoices. 
        :type support_invoice: bool
        
        :param can_use_restricted: Set to true to allow use restricted directions. 
        :type can_use_restricted: bool
        
        :param min_payment_amount: The minimum payment amount. 
        :type min_payment_amount: int
        
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

        if min_payment_amount is not None:
            params['min_payment_amount']=min_payment_amount

        
        res = self._perform_request('SetChildAccountInfo', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_currency_rate(self, currency, date=None):
        """
        Gets the exchange rate on selected date (per USD).

        
        :param currency: The currency code list. Examples: RUR, EUR, USD 
        :type currency: list | string
        
        :param date: The date, format: YYYY-MM-DD 
        :type date: datetime.date
        
        :rtype: dict
        """
        params = dict()
        
        params['currency']=self._serialize_list(currency)

        
        if date is not None:
            params['date']=date

        
        res = self._perform_request('GetCurrencyRate', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
                self._preprocess_exchange_rates(res["result"])
        return res

    def get_resource_price(self, resource_type=None, price_group_id=None, price_group_name=None, resource_param=None):
        """
        Gets the resource price.

        
        :param resource_type: The resource type list. The possible values are: ASR, AUDIORECORD, PSTN_IN_GB, PSTN_IN_GEOGRAPHIC, PSTN_IN_RU, PSTN_IN_RU_TOLLFREE, PSTN_IN_US, PSTN_IN_US_TF, PSTNOUT, SIPOUT, SIPOUTVIDEO, VOIPIN, VOIPOUT, VOIPOUTVIDEO 
        :type resource_type: list | string
        
        :param price_group_id: The price group ID list. 
        :type price_group_id: list | int | string
        
        :param price_group_name: The price group name template to filter. 
        :type price_group_name: str
        
        :param resource_param: The resource parameter list. Example: a phone number list. 
        :type resource_param: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_resource_price(p)
        return res

    def get_subscription_price(self, subscription_template_id=None, subscription_template_type=None, subscription_template_name=None, count=None, offset=None):
        """
        Gets the subscription template price.

        
        :param subscription_template_id: The subscription template ID list. 
        :type subscription_template_id: list | int | string
        
        :param subscription_template_type: The subscription template type. The following values are possible: PHONE_NUM, SIP_REGISTRATION. 
        :type subscription_template_type: str
        
        :param subscription_template_name: The subscription template name  (example: SIP registration, Phone GB, Phone RU 495, ...). 
        :type subscription_template_name: str
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_subscription_template_type(p)
        return res

    def get_children_accounts(self, child_account_id=None, child_account_name=None, child_account_email=None, active=None, frozen=None, ignore_invalid_accounts=None, brief_output=None, medium_output=None, count=None, offset=None, order_by=None, return_live_balance=None):
        """
        Gets the info about all children accounts.

        
        :param child_account_id: The account ID list or the 'all' value. 
        :type child_account_id: list | int | string
        
        :param child_account_name: The child account name part to filter. 
        :type child_account_name: str
        
        :param child_account_email: The child ccount email to filter. 
        :type child_account_email: str
        
        :param active: The active flag to filter. 
        :type active: bool
        
        :param frozen: The frozen flag to filter. 
        :type frozen: bool
        
        :param ignore_invalid_accounts: Set true to ignore the invalid 'child_account_id' items. 
        :type ignore_invalid_accounts: bool
        
        :param brief_output: Set true to output the account_id only. 
        :type brief_output: bool
        
        :param medium_output: Set true to output the account_id, account_name, account_email only. 
        :type medium_output: bool
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :param order_by: The following values are available: 'child_account_id', 'child_account_name' and 'child_account_email'. 
        :type order_by: str
        
        :param return_live_balance: Set true to get the user live balance. 
        :type return_live_balance: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_account_info_type(p)
        return res

    def transfer_money_to_child_account(self, child_account_id, amount, currency=None, strict_mode=None, child_transaction_description=None, parent_transaction_description=None, payment_reference=None, check_duplicate_reference_from=None):
        """
        Transfer the parent account's money to the child account or transfer the child's money to the parent account if the money amount is negative.

        
        :param child_account_id: The child account ID list. 
        :type child_account_id: list | int | string
        
        :param amount: The money amount, $. The absolute amount value must be equal or greater than 0.01 
        :type amount: decimal
        
        :param currency: The amount currency (the parent account currency by default). Examples: RUR, EUR, USD. 
        :type currency: str
        
        :param strict_mode: Returns error if strict_mode is true and an child account or the parent account hasn't enough money. 
        :type strict_mode: bool
        
        :param child_transaction_description: The child account transaction description. 
        :type child_transaction_description: str
        
        :param parent_transaction_description: The parent account transaction description. The following macro available: ${child_account_id}, ${child_account_name} 
        :type parent_transaction_description: str
        
        :param payment_reference: The external payment reference (extra info). 
        :type payment_reference: str
        
        :param check_duplicate_reference_from: Specify the date in 24-h format: YYYY-MM-DD HH:mm:ss to skip the duplicate transaction. 
        :type check_duplicate_reference_from: datetime.datetime
        
        :rtype: dict
        """
        params = dict()
        
        params['child_account_id']=self._serialize_list(child_account_id)

        params['amount']=amount

        
        if currency is not None:
            params['currency']=currency

        if strict_mode is not None:
            params['strict_mode']=strict_mode

        if child_transaction_description is not None:
            params['child_transaction_description']=child_transaction_description

        if parent_transaction_description is not None:
            params['parent_transaction_description']=parent_transaction_description

        if payment_reference is not None:
            params['payment_reference']=payment_reference

        if check_duplicate_reference_from is not None:
            params['check_duplicate_reference_from']=self._py_datetime_to_api(check_duplicate_reference_from)

        
        res = self._perform_request('TransferMoneyToChildAccount', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_money_amount_to_charge(self, currency=None, charge_date=None):
        """
        Get the recommended money amount to charge.

        
        :param currency: The currency name. Examples: USD, RUR, EUR. 
        :type currency: str
        
        :param charge_date: The next charge date, format: YYYY-MM-DD 
        :type charge_date: datetime.date
        
        :rtype: dict
        """
        params = dict()
        
        
        if currency is not None:
            params['currency']=currency

        if charge_date is not None:
            params['charge_date']=charge_date

        
        res = self._perform_request('GetMoneyAmountToCharge', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
                self._preprocess_get_money_amount_to_charge_result(res["result"])
        return res

    def charge_account(self, phone_id=None, phone_number=None):
        """
        Charges the account in the manual mode. You should call the ChargeAccount function to charge the subscriptions having the auto_charge=false.

        
        :param phone_id: The phone ID list or the 'all' value. You should specify the phones having the auto_charge=false. 
        :type phone_id: list | int | string
        
        :param phone_number: Can be used instead of <b>phone_id</b>. The phone number list or the 'all' value. You should specify the phones having the auto_charge=false. 
        :type phone_number: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
                self._preprocess_charge_account_result(res["result"])
        return res

    def add_application(self, application_name, secure_record_storage=None):
        """
        Adds a new account's application.

        
        :param application_name: The short application name in format \[a-z\]\[a-z0-9-\]{1,64} 
        :type application_name: str
        
        :param secure_record_storage: Enable secure storage for all logs and records of the application 
        :type secure_record_storage: bool
        
        :rtype: dict
        """
        params = dict()
        
        params['application_name']=application_name

        
        if secure_record_storage is not None:
            params['secure_record_storage']=secure_record_storage

        
        res = self._perform_request('AddApplication', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_application(self, application_id=None, application_name=None):
        """
        Deletes the account's application.

        
        :param application_id: The application ID list or the 'all' value. 
        :type application_id: list | int | string
        
        :param application_name: The application name list. Can be used instead of <b>appliction_id</b>. 
        :type application_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_application_info(self, application_id=None, required_application_name=None, application_name=None, secure_record_storage=None):
        """
        Edits the account's application.

        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param required_application_name: Can be used instead of <b>application_id</b>. 
        :type required_application_name: str
        
        :param application_name: The new short application name in format [a-z][a-z0-9-]{1,79} 
        :type application_name: str
        
        :param secure_record_storage: Enable secure storage for all logs and records of the application 
        :type secure_record_storage: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_applications(self, application_id=None, application_name=None, user_id=None, excluded_user_id=None, showing_user_id=None, with_rules=None, with_scenarios=None, count=None, offset=None):
        """
        Gets the account's applications.

        
        :param application_id: The application ID to filter. 
        :type application_id: int
        
        :param application_name: The application name part to filter. 
        :type application_name: str
        
        :param user_id: The user ID to filter. 
        :type user_id: int
        
        :param excluded_user_id: The excluded user ID to filter. 
        :type excluded_user_id: int
        
        :param showing_user_id: Specify the user ID value to show it in the 'users' array output. 
        :type showing_user_id: int
        
        :param with_rules: Set true to get bound rules info. 
        :type with_rules: bool
        
        :param with_scenarios: Set true to get bound rules and scenarios info. 
        :type with_scenarios: bool
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :rtype: dict
        """
        params = dict()
        
        
        if application_id is not None:
            params['application_id']=application_id

        if application_name is not None:
            params['application_name']=application_name

        if user_id is not None:
            params['user_id']=user_id

        if excluded_user_id is not None:
            params['excluded_user_id']=excluded_user_id

        if showing_user_id is not None:
            params['showing_user_id']=showing_user_id

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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_application_info_type(p)
        return res

    def add_user(self, user_name, user_display_name, user_password, application_id=None, application_name=None, mobile_phone=None, user_active=None, user_custom_data=None):
        """
        Adds a new user.

        
        :param user_name: The user name in format [a-z0-9][a-z0-9_-]{2,49} 
        :type user_name: str
        
        :param user_display_name: The user display name. The length must be less than 256. 
        :type user_display_name: str
        
        :param user_password: The user password. The length must be at least 6 symbols. 
        :type user_password: str
        
        :param application_id: The application ID which new user will be bound to. Could be used instead of the <b>application_name</b> parameter. 
        :type application_id: int
        
        :param application_name: The application name which new user will be bound to. Could be used instead of the <b>application_id</b> parameter. 
        :type application_name: str
        
        :param mobile_phone: The user mobile phone. The length must be less than 50. 
        :type mobile_phone: str
        
        :param user_active: The user enable flag 
        :type user_active: bool
        
        :param user_custom_data: Any string 
        :type user_custom_data: str
        
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

        if mobile_phone is not None:
            params['mobile_phone']=mobile_phone

        if user_active is not None:
            params['user_active']=user_active

        if user_custom_data is not None:
            params['user_custom_data']=user_custom_data

        
        res = self._perform_request('AddUser', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_user(self, user_id=None, user_name=None, application_id=None, application_name=None):
        """
        Deletes the specified user(s).

        
        :param user_id: The user ID list or the 'all' value. 
        :type user_id: list | int | string
        
        :param user_name: The user name list that can be used instead of <b>user_id</b>. 
        :type user_name: list | string
        
        :param application_id: Delete the specified users bound to the application ID. It is required if the <b>user_name</b> is specified. 
        :type application_id: int
        
        :param application_name: Delete the specified users bound to the application name. Could be used instead of the <b>application_id</b> parameter. 
        :type application_name: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_user_info(self, user_id=None, user_name=None, application_id=None, application_name=None, new_user_name=None, user_display_name=None, user_password=None, user_active=None, user_custom_data=None, mobile_phone=None):
        """
        Edits the user.

        
        :param user_id: The user to edit. 
        :type user_id: int
        
        :param user_name: Can be used instead of <b>user_id</b>. 
        :type user_name: str
        
        :param application_id: The application ID. It is required if the <b>user_name</b> is specified. 
        :type application_id: int
        
        :param application_name: The application name that can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param new_user_name: The new user name in format [a-z0-9][a-z0-9_-]{2,49} 
        :type new_user_name: str
        
        :param user_display_name: The new user display name. The length must be less than 256. 
        :type user_display_name: str
        
        :param user_password: The new user password. The length must be at least 6 symbols. 
        :type user_password: str
        
        :param user_active: The user enable flag 
        :type user_active: bool
        
        :param user_custom_data: Any string 
        :type user_custom_data: str
        
        :param mobile_phone: The new user mobile phone. The length must be less than 50. 
        :type mobile_phone: str
        
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

        if user_active is not None:
            params['user_active']=user_active

        if user_custom_data is not None:
            params['user_custom_data']=user_custom_data

        if mobile_phone is not None:
            params['mobile_phone']=mobile_phone

        
        res = self._perform_request('SetUserInfo', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_users(self, application_id=None, application_name=None, skill_id=None, excluded_skill_id=None, acd_queue_id=None, excluded_acd_queue_id=None, user_id=None, user_name=None, user_active=None, user_display_name=None, with_skills=None, with_queues=None, acd_status=None, showing_skill_id=None, count=None, offset=None, order_by=None, return_live_balance=None):
        """
        Shows the users of the specified account.

        
        :param application_id: The application ID to filter. 
        :type application_id: int
        
        :param application_name: The application name part to filter. 
        :type application_name: str
        
        :param skill_id: The skill ID to filter. 
        :type skill_id: int
        
        :param excluded_skill_id: The excluded skill ID to filter. 
        :type excluded_skill_id: int
        
        :param acd_queue_id: The ACD queue ID to filter. 
        :type acd_queue_id: int
        
        :param excluded_acd_queue_id: The excluded ACD queue ID to filter. 
        :type excluded_acd_queue_id: int
        
        :param user_id: The user ID to filter. 
        :type user_id: int
        
        :param user_name: The user name part to filter. 
        :type user_name: str
        
        :param user_active: The user active flag to filter. 
        :type user_active: bool
        
        :param user_display_name: The user display name part to filter. 
        :type user_display_name: str
        
        :param with_skills: Set true to get the bound skills. 
        :type with_skills: bool
        
        :param with_queues: Set true to get the bound queues. 
        :type with_queues: bool
        
        :param acd_status: The ACD status list to filter. The following values are possible: OFFLINE, ONLINE, READY, BANNED, IN_SERVICE, AFTER_SERVICE, TIMEOUT, DND. 
        :type acd_status: list | string
        
        :param showing_skill_id: The skill to show in the 'skills' field output. 
        :type showing_skill_id: int
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :param order_by: The following values are available: 'user_id', 'user_name' and 'user_display_name'. 
        :type order_by: str
        
        :param return_live_balance: Set true to get the user live balance. 
        :type return_live_balance: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_user_info_type(p)
        return res

    def create_call_list(self, rule_id, priority, max_simultaneous, num_attempts, name, file_content, interval_seconds=None, queue_id=None, avg_waiting_sec=None, encoding=None, delimiter=None, escape=None, reference_ip=None):
        """
        Adds a new CSV file for call list processing and starts the specified rule immediately. To send a file, use the request body. To set the call time constraints, use the options ____start_execution_time__ and ____end_execution_time__ in CSV file. Time is in UTC+0 24-h format: HH:mm:ss. <b>IMPORTANT:</b> the account's balance should be equal or greater than 1 USD. If the balance is lower than 1 USD, the call list processing won't start, or it stops immediately if it was active.

        
        :param rule_id: The rule ID. It's specified in the <a href='//manage.voximplant.com/#applications'>Applications</a> section of the Control Panel 
        :type rule_id: int
        
        :param priority: Call list priority. The value is in the range of [0 ... 2^31] where zero is the highest priority. 
        :type priority: int
        
        :param max_simultaneous: Number simultaneously processed tasks. 
        :type max_simultaneous: int
        
        :param num_attempts: Number of attempts. Minimum is <b>1</b>, maximum is <b>5</b>. 
        :type num_attempts: int
        
        :param name: File name, up to 255 characters and can't contain the '/' and '\' symbols. 
        :type name: str
        
        :param file_content: Send as "body" part of the HTTP request or as multiform. The sending "file_content" via URL is at its own risk because the network devices tend to drop HTTP requests with large headers. 
        :type file_content: str
        
        :param interval_seconds: Interval between call attempts in seconds. The default is 0. 
        :type interval_seconds: int
        
        :param queue_id: Queue Id. For processing call list with PDS (predictive dialer) the ID of the queue must be specified. 
        :type queue_id: int
        
        :param avg_waiting_sec: Average waiting time in the queue(seconds). Default is 1 
        :type avg_waiting_sec: int
        
        :param encoding: Encoding file. The default is UTF-8. 
        :type encoding: str
        
        :param delimiter: Separator values. The default is ';' 
        :type delimiter: str
        
        :param escape: Escape character. Used for parsing csv 
        :type escape: str
        
        :param reference_ip: Specifies the IP from the geolocation of call list subscribers. It allows selecting the nearest server for serving subscribers. 
        :type reference_ip: str
        
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

        if queue_id is not None:
            params['queue_id']=queue_id

        if avg_waiting_sec is not None:
            params['avg_waiting_sec']=avg_waiting_sec

        if encoding is not None:
            params['encoding']=encoding

        if delimiter is not None:
            params['delimiter']=delimiter

        if escape is not None:
            params['escape']=escape

        if reference_ip is not None:
            params['reference_ip']=reference_ip

        
        res = self._perform_request('CreateCallList', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def create_manual_call_list(self, rule_id, priority, max_simultaneous, num_attempts, name, file_content, interval_seconds=None, encoding=None, delimiter=None, escape=None, reference_ip=None):
        """
        Adds a new CSV file for manual call list processing and bind it with the specified rule. To send a file, use the request body. To start processing calls, use the function <a href='//voximplant.com/docs/references/httpapi/managing_call_lists#startnextcalltask'>StartNextCallTask</a>. <b>IMPORTANT:</b> the account's balance should be equal or greater than 1 USD. If the balance is lower than 1 USD, the call list processing won't start, or it stops immediately if it was active.

        
        :param rule_id: The rule ID. 
        :type rule_id: int
        
        :param priority: Call list priority. The value is in the range of [0 ... 2^31] where zero is the highest priority. 
        :type priority: int
        
        :param max_simultaneous: Number simultaneously processed tasks. 
        :type max_simultaneous: int
        
        :param num_attempts: Number of attempts. Should be equal or greater than <b>1</b> 
        :type num_attempts: int
        
        :param name: File name. 
        :type name: str
        
        :param file_content: Send as "body" part of the HTTP request or as multiform. The sending "file_content" via URL is at its own risk because the network devices tend to drop HTTP requests with large headers. 
        :type file_content: str
        
        :param interval_seconds: Interval between call attempts in seconds. The default is 0. 
        :type interval_seconds: int
        
        :param encoding: Encoding file. The default is UTF-8. 
        :type encoding: str
        
        :param delimiter: Separator values. The default is ';' 
        :type delimiter: str
        
        :param escape: Escape character. Used for parsing csv 
        :type escape: str
        
        :param reference_ip: Specifies the IP from the geolocation of call list subscribers. It allows selecting the nearest server for serving subscribers. 
        :type reference_ip: str
        
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

        
        res = self._perform_request('CreateManualCallList', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def start_next_call_task(self, list_id, custom_params=None):
        """
        Start processing the next task.

        
        :param list_id: The list Id. Can use a set of identifiers with the separator ";" 
        :type list_id: int
        
        :param custom_params: The custom param. Use to transfer the call initiator parameters to the scenario. 
        :type custom_params: str
        
        :rtype: dict
        """
        params = dict()
        
        params['list_id']=list_id

        
        if custom_params is not None:
            params['custom_params']=custom_params

        
        res = self._perform_request('StartNextCallTask', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def append_to_call_list(self, file_content, list_id=None, list_name=None, encoding=None, escape=None, delimiter=None):
        """
        Appending a new task to the existing call list.

        
        :param file_content: Send as Body Request or multiform. 
        :type file_content: str
        
        :param list_id: The call list ID 
        :type list_id: int
        
        :param list_name: Can be used instead of <b>list_id</b>. The unique name call list 
        :type list_name: str
        
        :param encoding: Encoding file. The default is UTF-8. 
        :type encoding: str
        
        :param escape: Escape character. Used for parsing csv 
        :type escape: str
        
        :param delimiter: Separator values. The default is ';' 
        :type delimiter: str
        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if list_id is not None:
            passed_args.append('list_id')
        if list_name is not None:
            passed_args.append('list_name')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into append_to_call_list")
        if len(passed_args) == 0:
            raise VoximplantException("None of list_id, list_name passed into append_to_call_list")
        
        
        params['file_content']=file_content

        
        if list_id is not None:
            params['list_id']=list_id

        if list_name is not None:
            params['list_name']=list_name

        if encoding is not None:
            params['encoding']=encoding

        if escape is not None:
            params['escape']=escape

        if delimiter is not None:
            params['delimiter']=delimiter

        
        res = self._perform_request('AppendToCallList', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_call_lists(self, name=None, is_active=None, from_date=None, to_date=None, type_list=None, count=None, offset=None):
        """
        Get all call lists for the specified user.

        
        :param name: Find call lists by name 
        :type name: str
        
        :param is_active: Find only active call lists 
        :type is_active: bool
        
        :param from_date: The UTC 'from' date filter in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type from_date: datetime.datetime
        
        :param to_date: The UTC 'to' date filter in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type to_date: datetime.datetime
        
        :param type_list: The type of call list. Available values: AUTOMATIC and MANUAL 
        :type type_list: str
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :rtype: dict
        """
        params = dict()
        
        
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

        
        res = self._perform_request('GetCallLists', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_call_list_type(p)
        return res

    def get_call_list_details(self, list_id, count=None, offset=None, output=None, encoding=None, delimiter=None):
        """
        Get details of the specified call list. Returns a CSV file by default.

        
        :param list_id: The list ID. 
        :type list_id: int
        
        :param count: Maximum number of entries in the result 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :param output: Output format (CSV/JSON/XLS). Default CSV 
        :type output: str
        
        :param encoding: Encoding of the output file. Default UTF-8 
        :type encoding: str
        
        :param delimiter: Separator values. The default is ';' 
        :type delimiter: str
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_call_list_detail_type(p)
        return res

    def stop_call_list_processing(self, list_id):
        """
        Stop processing the specified call list.

        
        :param list_id: The list Id. 
        :type list_id: int
        
        :rtype: dict
        """
        params = dict()
        
        params['list_id']=list_id

        
        
        res = self._perform_request('StopCallListProcessing', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def recover_call_list(self, list_id):
        """
        Resume processing the specified call list.

        
        :param list_id: The list Id. 
        :type list_id: int
        
        :rtype: dict
        """
        params = dict()
        
        params['list_id']=list_id

        
        
        res = self._perform_request('RecoverCallList', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def add_scenario(self, scenario_name, scenario_script, rewrite=None):
        """
        Adds a new scenario. Please use the POST method.

        
        :param scenario_name: The scenario name. The length must be less than 30 
        :type scenario_name: str
        
        :param scenario_script: The scenario text. The length must be less than 128 KB. 
        :type scenario_script: str
        
        :param rewrite: Is the existing scenario rewrite? 
        :type rewrite: bool
        
        :rtype: dict
        """
        params = dict()
        
        params['scenario_name']=scenario_name

        params['scenario_script']=scenario_script

        
        if rewrite is not None:
            params['rewrite']=rewrite

        
        res = self._perform_request('AddScenario', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_scenario(self, scenario_id=None, scenario_name=None):
        """
        Deletes the scenario.

        
        :param scenario_id: The scenario ID list or the 'all' value. 
        :type scenario_id: list | int | string
        
        :param scenario_name: Can be used instead of <b>scenario_id</b>. The scenario name list. 
        :type scenario_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def bind_scenario(self, scenario_id=None, scenario_name=None, rule_id=None, rule_name=None, application_id=None, application_name=None, bind=None):
        """
        Bind the scenario list to the rule. You should specify the application_id or application_name if you specify the rule_name.

        
        :param scenario_id: The scenario ID list. 
        :type scenario_id: list | int | string
        
        :param scenario_name: Can be used instead of <b>scenario_id</b>. The scenario name list. 
        :type scenario_name: list | string
        
        :param rule_id: The rule ID. 
        :type rule_id: int
        
        :param rule_name: The rule name that can be used instead of <b>rule_id</b>.  
        :type rule_name: str
        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param application_name: The application name that can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param bind: Bind or unbind? 
        :type bind: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_scenarios(self, scenario_id=None, scenario_name=None, with_script=None, count=None, offset=None):
        """
        Gets the account's scenarios.

        
        :param scenario_id: The scenario ID to filter 
        :type scenario_id: int
        
        :param scenario_name: The scenario name to filter. Can be used instead of <b>scenario_id</b>. All scenarios containing this param in their names will be returned. The parameter is case insensitive. 
        :type scenario_name: str
        
        :param with_script: Set true to get the scenario text. You must specify the 'scenario_id' too! 
        :type with_script: bool
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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

        
        res = self._perform_request('GetScenarios', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_scenario_info_type(p)
        return res

    def set_scenario_info(self, scenario_id=None, required_scenario_name=None, scenario_name=None, scenario_script=None):
        """
        Edits the scenario. Please use the POST method.

        
        :param scenario_id: The scenario ID. 
        :type scenario_id: int
        
        :param required_scenario_name: The name of the scenario to edit, can be used instead of <b>scenario_id</b>. 
        :type required_scenario_name: str
        
        :param scenario_name: The new scenario name. The length must be less than 30 
        :type scenario_name: str
        
        :param scenario_script: The new scenario text. The length must be less than 128 KB. 
        :type scenario_script: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def reorder_scenarios(self, rule_id=None, rule_name=None, scenario_id=None):
        """
        Configures the order of the rules that are assigned to the specified rule.

        
        :param rule_id: The rule ID. 
        :type rule_id: int
        
        :param rule_name: The rule name that can be used instead of <b>rule_id</b>. 
        :type rule_name: str
        
        :param scenario_id: The scenario ID list. 
        :type scenario_id: list | int | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def start_scenarios(self, rule_id, user_id=None, user_name=None, application_id=None, application_name=None, script_custom_data=None, reference_ip=None):
        """
        Run the JavaScript scenarios on a VoxImplant server. The scenarios run in a new media session.

        
        :param rule_id: The rule ID. 
        :type rule_id: int
        
        :param user_id: The user ID. Run the scripts from the user if set. 
        :type user_id: int
        
        :param user_name: The user name that can be used instead of <b>user_id</b>. Run the scripts from the user if set. 
        :type user_name: str
        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param application_name: The application name that can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param script_custom_data: The script custom data (like a script argument). Can be accessed in JS scenario via the <a href='//voximplant.com/docs/references/voxengine/voxengine#customdata'>VoxEngine.customData()</a> method 
        :type script_custom_data: str
        
        :param reference_ip: Specifies the IP from the geolocation of predicted subscribers. It allows selecting the nearest server for serving subscribers. 
        :type reference_ip: str
        
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

        
        res = self._perform_request('StartScenarios', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def start_conference(self, conference_name, rule_id, user_id=None, user_name=None, application_id=None, application_name=None, script_custom_data=None, reference_ip=None):
        """
        Start a new conference or join the conference.

        
        :param conference_name: The conference name. The name length must be less than 50 symbols. 
        :type conference_name: str
        
        :param rule_id: The rule ID. 
        :type rule_id: int
        
        :param user_id: The user ID. Run the scripts from the user if set. 
        :type user_id: int
        
        :param user_name: The user name that can be used instead of <b>user_id</b>. Run the scripts from the user if set. 
        :type user_name: str
        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param application_name: The application name that can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param script_custom_data: The script custom data (like a script argument). Can be accessed in JS scenario via the <a href='//voximplant.com/docs/references/voxengine/voxengine#customdata'>VoxEngine.customData()</a> method 
        :type script_custom_data: str
        
        :param reference_ip: Specifies the IP from the geolocation of predicted subscribers. It allows selecting the nearest server for serving subscribers. 
        :type reference_ip: str
        
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

        
        res = self._perform_request('StartConference', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def add_rule(self, rule_name, rule_pattern, application_id=None, application_name=None, rule_pattern_exclude=None, video_conference=None, scenario_id=None, scenario_name=None):
        """
        Adds a new rule for the application.

        
        :param rule_name: The rule name. The length must be less than 100 
        :type rule_name: str
        
        :param rule_pattern: The rule pattern regex. The length must be less than 64 KB. 
        :type rule_pattern: str
        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param application_name: The application name, can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param rule_pattern_exclude: The exclude pattern regex. The length must be less than 64 KB. 
        :type rule_pattern_exclude: str
        
        :param video_conference: Is video conference required? 
        :type video_conference: bool
        
        :param scenario_id: The scenario ID list. 
        :type scenario_id: list | int | string
        
        :param scenario_name: Can be used instead of <b>scenario_id</b>. The scenario name list. 
        :type scenario_name: list | string
        
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

        if scenario_id is not None:
            params['scenario_id']=self._serialize_list(scenario_id)

        if scenario_name is not None:
            params['scenario_name']=self._serialize_list(scenario_name)

        
        res = self._perform_request('AddRule', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_rule(self, rule_id=None, rule_name=None, application_id=None, application_name=None):
        """
        Deletes the rule.

        
        :param rule_id: The rule ID list or the 'all' value. 
        :type rule_id: list | int | string
        
        :param rule_name: Can be used instead of <b>rule_id</b>. The rule name list. 
        :type rule_name: list | string
        
        :param application_id: The application ID list or the 'all' value. 
        :type application_id: list | int | string
        
        :param application_name: Can be used instead of <b>application_id</b>. The application name list. 
        :type application_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_rule_info(self, rule_id, rule_name=None, rule_pattern=None, rule_pattern_exclude=None, video_conference=None):
        """
        Edits the rule.

        
        :param rule_id: The rule ID. 
        :type rule_id: int
        
        :param rule_name: The new rule name. The length must be less than 100 
        :type rule_name: str
        
        :param rule_pattern: The new rule pattern regex. The length must be less than 64 KB. 
        :type rule_pattern: str
        
        :param rule_pattern_exclude: The new exclude pattern regex. The length must be less than 64 KB. 
        :type rule_pattern_exclude: str
        
        :param video_conference: Is video conference required? 
        :type video_conference: bool
        
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

        
        res = self._perform_request('SetRuleInfo', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_rules(self, application_id=None, application_name=None, rule_id=None, rule_name=None, video_conference=None, template=None, with_scenarios=None, count=None, offset=None):
        """
        Gets the rules.

        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param application_name: The application name that can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param rule_id: The rule ID to filter 
        :type rule_id: int
        
        :param rule_name: The rule name part to filter. 
        :type rule_name: str
        
        :param video_conference: The video conference flag to filter. 
        :type video_conference: bool
        
        :param template: Search for template matching 
        :type template: str
        
        :param with_scenarios: Set true to get bound scenarios info. 
        :type with_scenarios: bool
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_rule_info_type(p)
        return res

    def reorder_rules(self, rule_id):
        """
        Configures the rules' order in the <a href='//manage.voximplant.com/#editApplication'>Applications</a> section of Control panel. Note: the rules must belong to the same application!

        
        :param rule_id: The rule ID list. 
        :type rule_id: list | int | string
        
        :rtype: dict
        """
        params = dict()
        
        params['rule_id']=self._serialize_list(rule_id)

        
        
        res = self._perform_request('ReorderRules', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_call_history(self, from_date, to_date, call_session_history_id=None, application_id=None, application_name=None, user_id=None, rule_name=None, remote_number=None, local_number=None, call_session_history_custom_data=None, with_calls=None, with_records=None, with_other_resources=None, child_account_id=None, children_calls_only=None, with_header=None, desc_order=None, with_total_count=None, count=None, offset=None, output=None, is_async=None):
        """
        Gets the call history.

        
        :param from_date: The from date in the selected timezone in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type from_date: datetime.datetime
        
        :param to_date: The to date in the selected timezone in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type to_date: datetime.datetime
        
        :param call_session_history_id: The call session history ID list. The sessions IDs can be accessed in JS scenario via the <b>sessionID</b> property of the <a href='//voximplant.com/docs/references/voxengine/appevents#started'>AppEvents.Started</a> event 
        :type call_session_history_id: list | int | string
        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param application_name: The application name, can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param user_id: The user ID list. If it's specified the output will contain only calls from/to any VoxImplant SDK related to the specified user. 
        :type user_id: list | int | string
        
        :param rule_name: The rule name to filter. 
        :type rule_name: str
        
        :param remote_number: The remote number list. 
        :type remote_number: list | string
        
        :param local_number: The local number list. 
        :type local_number: list | string
        
        :param call_session_history_custom_data: The custom_data to filter sessions. 
        :type call_session_history_custom_data: str
        
        :param with_calls: Set true to get the bound calls. 
        :type with_calls: bool
        
        :param with_records: Set true to get the bound records. 
        :type with_records: bool
        
        :param with_other_resources: Set true to get other resources usage (see [ResourceUsageType]). 
        :type with_other_resources: bool
        
        :param child_account_id: The child account ID list or the 'all' value. 
        :type child_account_id: list | int | string
        
        :param children_calls_only: Set true to get the children account calls only. 
        :type children_calls_only: bool
        
        :param with_header: Set false to get a CSV file without the column names if the output=csv 
        :type with_header: bool
        
        :param desc_order: Set true to get records in the descent order. 
        :type desc_order: bool
        
        :param with_total_count: Set false to omit the 'total_count' and increase performance. 
        :type with_total_count: bool
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :param output: The output format. The following values available: json, csv. 
        :type output: str
        
        :param is_async: Set true to get records in the asynchronous mode (for csv output only). If it's true, the request could be available via <a href='//voximplant.com/docs/references/httpapi/managing_history#gethistoryreports'>GetHistoryReports</a> and <a href='//voximplant.com/docs/references/httpapi/managing_history#downloadhistoryreport'>DownloadHistoryReport</a> methods. 
        :type is_async: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_call_session_info_type(p)
        return res

    def get_history_reports(self, history_report_id=None, history_type=None, created_from=None, created_to=None, is_completed=None, desc_order=None, count=None, offset=None):
        """
        Gets the list of history reports and their statuses. The method returns info about reports made via [GetCallHistory] with the specified __output=csv__ and **is_async=true** parameters.

        
        :param history_report_id: The history report ID to filter 
        :type history_report_id: int
        
        :param history_type: The history report type list or the 'all' value. The following values are possible: calls, transactions, audit, call_list. 
        :type history_type: list | string
        
        :param created_from: The UTC creation from date filter in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type created_from: datetime.datetime
        
        :param created_to: The UTC creation to date filter in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type created_to: datetime.datetime
        
        :param is_completed: Is report completed? 
        :type is_completed: bool
        
        :param desc_order: Set true to get records in the descent order. 
        :type desc_order: bool
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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

        
        res = self._perform_request('GetHistoryReports', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_history_report_type(p)
        return res

    def download_history_report(self, history_report_id):
        """
        Downloads the required history report.

        
        :param history_report_id: The history report ID. 
        :type history_report_id: int
        
        :rtype: dict
        """
        params = dict()
        
        params['history_report_id']=history_report_id

        
        
        res = self._perform_request('DownloadHistoryReport', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
                self._preprocess_None(res["result"])
        return res

    def get_transaction_history(self, from_date, to_date, transaction_id=None, payment_reference=None, transaction_type=None, user_id=None, child_account_id=None, children_transactions_only=None, users_transactions_only=None, desc_order=None, count=None, offset=None, output=None, is_async=None):
        """
        Gets the transaction history.

        
        :param from_date: The from date in the selected timezone in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type from_date: datetime.datetime
        
        :param to_date: The to date in the selected timezone in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type to_date: datetime.datetime
        
        :param transaction_id: The transaction ID list. 
        :type transaction_id: list | int | string
        
        :param payment_reference: The external payment reference to filter. 
        :type payment_reference: str
        
        :param transaction_type: The transaction type list. The following values are possible: periodic_charge, resource_charge, money_distribution, subscription_charge, subscription_installation_charge, card_periodic_payment, card_overrun_payment, card_payment, robokassa_payment, gift, add_money, subscription_cancel, adjustment, wire_transfer, refund. 
        :type transaction_type: list | string
        
        :param user_id: The user ID list. 
        :type user_id: list | int | string
        
        :param child_account_id: The child account ID list or the 'all' value. 
        :type child_account_id: list | int | string
        
        :param children_transactions_only: Set true to get the children account transactions only. 
        :type children_transactions_only: bool
        
        :param users_transactions_only: Set true to get the users' transactions only. 
        :type users_transactions_only: bool
        
        :param desc_order: Set true to get records in the descent order. 
        :type desc_order: bool
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :param output: The output format. The following values available: json, csv 
        :type output: str
        
        :param is_async: Set true to get records in the asynchronous mode (for csv output only). See the [GetHistoryReports], [DownloadHistoryReport] functions. 
        :type is_async: bool
        
        :rtype: dict
        """
        params = dict()
        
        params['from_date']=self._py_datetime_to_api(from_date)

        params['to_date']=self._py_datetime_to_api(to_date)

        
        if transaction_id is not None:
            params['transaction_id']=self._serialize_list(transaction_id)

        if payment_reference is not None:
            params['payment_reference']=payment_reference

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

        
        res = self._perform_request('GetTransactionHistory', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_transaction_info_type(p)
        return res

    def delete_record(self, record_url=None, record_id=None):
        """
        Try to remove record and transcription files.

        
        :param record_url: Url to remove. 
        :type record_url: str
        
        :param record_id: The record id for remove. 
        :type record_id: int
        
        :rtype: dict
        """
        params = dict()
        
        
        if record_url is not None:
            params['record_url']=record_url

        if record_id is not None:
            params['record_id']=record_id

        
        res = self._perform_request('DeleteRecord', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_acd_history(self, from_date, to_date, acd_session_history_id=None, acd_request_id=None, acd_queue_id=None, user_id=None, operator_hangup=None, unserviced=None, min_waiting_time=None, rejected=None, with_events=None, with_header=None, desc_order=None, count=None, offset=None, output=None):
        """
        Gets the ACD history.

        
        :param from_date: The UTC 'from' date filter in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type from_date: datetime.datetime
        
        :param to_date: The UTC 'to' date filter in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type to_date: datetime.datetime
        
        :param acd_session_history_id: The ACD session history ID list. 
        :type acd_session_history_id: list | int | string
        
        :param acd_request_id: The ACD request ID list. 
        :type acd_request_id: list | string
        
        :param acd_queue_id: The ACD queue ID list to filter. 
        :type acd_queue_id: list | int | string
        
        :param user_id: The user ID list to filter. 
        :type user_id: list | int | string
        
        :param operator_hangup: Set true to get the calls terminated by the operator. 
        :type operator_hangup: bool
        
        :param unserviced: The unserviced calls by the operator. 
        :type unserviced: bool
        
        :param min_waiting_time: The min waiting time filter. 
        :type min_waiting_time: int
        
        :param rejected: The rejected calls by the 'max_queue_size', 'max_waiting_time' threshold. 
        :type rejected: bool
        
        :param with_events: Set true to get the bound events. 
        :type with_events: bool
        
        :param with_header: Set false to get a CSV file without the column names if the output=csv 
        :type with_header: bool
        
        :param desc_order: Set true to get records in the descent order. 
        :type desc_order: bool
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :param output: The output format. The following values available: json, csv 
        :type output: str
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_acd_session_info_type(p)
        return res

    def get_audit_log(self, from_date, to_date, audit_log_id=None, filtered_admin_user_id=None, filtered_ip=None, filtered_cmd=None, advanced_filters=None, with_header=None, desc_order=None, with_total_count=None, count=None, offset=None, output=None, is_async=None):
        """
        Gets the history of account changes.

        
        :param from_date: The UTC 'from' date filter in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type from_date: datetime.datetime
        
        :param to_date: The UTC 'to' date filter in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type to_date: datetime.datetime
        
        :param audit_log_id: The audit history ID list. 
        :type audit_log_id: list | int | string
        
        :param filtered_admin_user_id: The admin user ID to filter. 
        :type filtered_admin_user_id: str
        
        :param filtered_ip: The IP list to filter. 
        :type filtered_ip: list | string
        
        :param filtered_cmd: The function list to filter. 
        :type filtered_cmd: list | string
        
        :param advanced_filters: A relation ID to filter (for example: a phone_number value, a user_id value, an application_id value). 
        :type advanced_filters: str
        
        :param with_header: Set false to get a CSV file without the column names if the output=csv 
        :type with_header: bool
        
        :param desc_order: Set true to get records in the descent order. 
        :type desc_order: bool
        
        :param with_total_count: Set false to omit the 'total_count' and increase performance. 
        :type with_total_count: bool
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :param output: The output format. The following values available: json, csv. 
        :type output: str
        
        :param is_async: Set true to get records in the asynchronous mode (for csv output only). If it's true, the request could be available via <a href='//voximplant.com/docs/references/httpapi/managing_history#gethistoryreports'>GetHistoryReports</a> and <a href='//voximplant.com/docs/references/httpapi/managing_history#downloadhistoryreport'>DownloadHistoryReport</a> methods. 
        :type is_async: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_audit_log_info_type(p)
        return res

    def add_pstn_black_list_item(self, pstn_blacklist_phone):
        """
        Add a new phone number to the PSTN blacklist. BlackList works for numbers that are purchased from Voximplant only. Since we have no control over exact phone number format for calls from SIP integrations, blacklisting such numbers should be done via JavaScript scenarios.

        
        :param pstn_blacklist_phone: The phone number in format e164 or regex pattern 
        :type pstn_blacklist_phone: str
        
        :rtype: dict
        """
        params = dict()
        
        params['pstn_blacklist_phone']=pstn_blacklist_phone

        
        
        res = self._perform_request('AddPstnBlackListItem', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_pstn_black_list_item(self, pstn_blacklist_id, pstn_blacklist_phone):
        """
        Update the PSTN blacklist item. BlackList works for numbers that are purchased from Voximplant only. Since we have no control over exact phone number format for calls from SIP integrations, blacklisting such numbers should be done via JavaScript scenarios.

        
        :param pstn_blacklist_id: The PSTN black list item ID. 
        :type pstn_blacklist_id: int
        
        :param pstn_blacklist_phone: The new phone number in format e164. 
        :type pstn_blacklist_phone: str
        
        :rtype: dict
        """
        params = dict()
        
        params['pstn_blacklist_id']=pstn_blacklist_id

        params['pstn_blacklist_phone']=pstn_blacklist_phone

        
        
        res = self._perform_request('SetPstnBlackListItem', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_pstn_black_list_item(self, pstn_blacklist_id):
        """
        Remove phone number from the PSTN blacklist.

        
        :param pstn_blacklist_id: The PSTN black list item ID. 
        :type pstn_blacklist_id: int
        
        :rtype: dict
        """
        params = dict()
        
        params['pstn_blacklist_id']=pstn_blacklist_id

        
        
        res = self._perform_request('DelPstnBlackListItem', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_pstn_black_list(self, pstn_blacklist_id=None, pstn_blacklist_phone=None, count=None, offset=None):
        """
        Get the whole PSTN blacklist.

        
        :param pstn_blacklist_id: The PSTN black list item ID for filter. 
        :type pstn_blacklist_id: int
        
        :param pstn_blacklist_phone: The phone number in format e164 for filter. 
        :type pstn_blacklist_phone: str
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_pstn_black_list_info_type(p)
        return res

    def add_sip_white_list_item(self, sip_whitelist_network):
        """
        Adds a new network address to the SIP white list.

        
        :param sip_whitelist_network: The network address in format A.B.C.D/L or A.B.C.D/a.b.c.d (example 192.168.1.5/16). 
        :type sip_whitelist_network: str
        
        :rtype: dict
        """
        params = dict()
        
        params['sip_whitelist_network']=sip_whitelist_network

        
        
        res = self._perform_request('AddSipWhiteListItem', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_sip_white_list_item(self, sip_whitelist_id):
        """
        Deletes the network address from the SIP white list.

        
        :param sip_whitelist_id: The SIP white list item ID to delete. 
        :type sip_whitelist_id: int
        
        :rtype: dict
        """
        params = dict()
        
        params['sip_whitelist_id']=sip_whitelist_id

        
        
        res = self._perform_request('DelSipWhiteListItem', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_sip_white_list_item(self, sip_whitelist_id, sip_whitelist_network):
        """
        Edits the SIP white list.

        
        :param sip_whitelist_id: The SIP white list item ID 
        :type sip_whitelist_id: int
        
        :param sip_whitelist_network: The new network address in format A.B.C.D/L or A.B.C.D/a.b.c.d (example 192.168.1.5/16) 
        :type sip_whitelist_network: str
        
        :rtype: dict
        """
        params = dict()
        
        params['sip_whitelist_id']=sip_whitelist_id

        params['sip_whitelist_network']=sip_whitelist_network

        
        
        res = self._perform_request('SetSipWhiteListItem', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_sip_white_list(self, sip_whitelist_id=None, count=None, offset=None):
        """
        Gets the SIP white list.

        
        :param sip_whitelist_id: The SIP white list item ID to filter 
        :type sip_whitelist_id: int
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_sip_white_list_info_type(p)
        return res

    def create_sip_registration(self, sip_username, proxy, auth_user=None, outbound_proxy=None, password=None, is_persistent=None, application_id=None, application_name=None, rule_id=None, rule_name=None, user_id=None, user_name=None):
        """
        Create a new SIP registration. You should specify the application_id or application_name if you specify the rule_name or user_id, or user_name. You should set is_persistent=true if you specify the user_id or user_name. You can bind only one SIP registration to the user (the previous SIP registration will be auto unbound).

        
        :param sip_username: The user name. 
        :type sip_username: str
        
        :param proxy: The SIP proxy 
        :type proxy: str
        
        :param auth_user: The SIP authentications user 
        :type auth_user: str
        
        :param outbound_proxy: The outbound SIP proxy 
        :type outbound_proxy: str
        
        :param password: The SIP password 
        :type password: str
        
        :param is_persistent: Is SIP registration persistent or on the user logon? 
        :type is_persistent: bool
        
        :param application_id: The application ID which new SIP registration will be bound to. Could be used instead of the <b>application_name</b> parameter. 
        :type application_id: int
        
        :param application_name: The application name which new SIP registration will be bound to. Could be used instead of the <b>application_id</b> parameter. 
        :type application_name: str
        
        :param rule_id: The rule ID which new SIP registration will be bound to. Could be used instead of the <b>rule_name</b> parameter. 
        :type rule_id: int
        
        :param rule_name: The rule name which new SIP registration will be bound to. Could be used instead of the <b>rule_id</b> parameter. 
        :type rule_name: str
        
        :param user_id: The user ID which new SIP registration will be bound to. Could be used instead of the <b>user_name</b> parameter. 
        :type user_id: int
        
        :param user_name: The user name which new SIP registration will be bound to. Could be used instead of the <b>user_id</b> parameter. 
        :type user_name: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def update_sip_registration(self, sip_registration_id, sip_username=None, proxy=None, auth_user=None, outbound_proxy=None, password=None, application_id=None, application_name=None, rule_id=None, rule_name=None, user_id=None, user_name=None):
        """
        Update SIP registration. You should specify the application_id or application_name if you specify the rule_name or user_id, or user_name. You can bind only one SIP registration to the user (the previous SIP registration will be auto unbound).

        
        :param sip_registration_id: The registration ID 
        :type sip_registration_id: int
        
        :param sip_username: The user name. 
        :type sip_username: str
        
        :param proxy: The SIP proxy 
        :type proxy: str
        
        :param auth_user: The SIP authentications user 
        :type auth_user: str
        
        :param outbound_proxy: The outbound SIP proxy 
        :type outbound_proxy: str
        
        :param password: The SIP password 
        :type password: str
        
        :param application_id: The application ID which the SIP registration will be bound to. Could be used instead of the <b>application_name</b> parameter. 
        :type application_id: int
        
        :param application_name: The application name which the SIP registration will be bound to. Could be used instead of the <b>application_id</b> parameter. 
        :type application_name: str
        
        :param rule_id: The rule ID which the SIP registration will be bound to. Could be used instead of the <b>rule_name</b> parameter. 
        :type rule_id: int
        
        :param rule_name: The rule name which the SIP registration will be bound to. Could be used instead of the <b>rule_id</b> parameter. 
        :type rule_name: str
        
        :param user_id: The user ID which the SIP registration will be bound to. Could be used instead of the <b>user_name</b> parameter. 
        :type user_id: int
        
        :param user_name: The user name which the SIP registration will be bound to. Could be used instead of the <b>user_id</b> parameter. 
        :type user_name: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def bind_sip_registration(self, sip_registration_id=None, application_id=None, application_name=None, rule_id=None, rule_name=None, user_id=None, user_name=None, bind=None):
        """
        Bind the SIP registration to the application/user or unbind the SIP registration from the application/user. You should specify the application_id or application_name if you specify the rule_name or user_id, or user_name. You should specify the sip_registration_id if you set bind=true. You can bind only one SIP registration to the user (the previous SIP registration will be auto unbound).

        
        :param sip_registration_id: The registration ID 
        :type sip_registration_id: int
        
        :param application_id: The application ID which the SIP registration will be bound to. Could be used instead of the <b>application_name</b> parameter. 
        :type application_id: int
        
        :param application_name: The application name which the SIP registration will be bound to. Could be used instead of the <b>application_id</b> parameter. 
        :type application_name: str
        
        :param rule_id: The rule ID which the SIP registration will be bound to. Could be used instead of the <b>rule_name</b> parameter. 
        :type rule_id: int
        
        :param rule_name: The rule name which the SIP registration will be bound to. Could be used instead of the <b>rule_id</b> parameter. 
        :type rule_name: str
        
        :param user_id: The user ID which the SIP registration will be bound to. Could be used instead of the <b>user_name</b> parameter. 
        :type user_id: int
        
        :param user_name: The user name which the SIP registration will be bound to. Could be used instead of the <b>user_id</b> parameter. 
        :type user_name: str
        
        :param bind: Bind or unbind? 
        :type bind: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def delete_sip_registration(self, sip_registration_id):
        """
        Delete SIP registration.

        
        :param sip_registration_id: The registration ID 
        :type sip_registration_id: int
        
        :rtype: dict
        """
        params = dict()
        
        params['sip_registration_id']=sip_registration_id

        
        
        res = self._perform_request('DeleteSipRegistration', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_sip_registrations(self, sip_registration_id=None, sip_username=None, deactivated=None, successful=None, is_persistent=None, application_id=None, application_name=None, is_bound_to_application=None, rule_id=None, rule_name=None, user_id=None, user_name=None, proxy=None, in_progress=None, status_code=None, count=None, offset=None):
        """
        Get active SIP registrations.

        
        :param sip_registration_id: The SIP registration ID. 
        :type sip_registration_id: int
        
        :param sip_username: The SIP user name to filter. 
        :type sip_username: str
        
        :param deactivated: Set true to show the frozen SIP registrations only. 
        :type deactivated: bool
        
        :param successful: Set false to show the unsuccessful SIP registrations only. 
        :type successful: bool
        
        :param is_persistent: The persistent flag to filter. 
        :type is_persistent: bool
        
        :param application_id: The application ID list to filter. Can be used instead of <b>appliction_name</b>. 
        :type application_id: list | int | string
        
        :param application_name: The application name list to filter. Can be used instead of <b>appliction_id</b>. 
        :type application_name: list | string
        
        :param is_bound_to_application: Is a SIP registration bound to an application. 
        :type is_bound_to_application: bool
        
        :param rule_id: The rule ID list to filter. Can be used instead of <b>rule_name</b>. 
        :type rule_id: list | int | string
        
        :param rule_name: The rule name list to filter. Can be used instead of <b>rule_id</b>. 
        :type rule_name: list | string
        
        :param user_id: The user ID list to filter. Can be used instead of <b>user_name</b>. 
        :type user_id: list | int | string
        
        :param user_name: The user name list to filter. Can be used instead of <b>user_id</b>. 
        :type user_name: list | string
        
        :param proxy: The list of proxy servers to use, divided by the ';' symbol. 
        :type proxy: list | string
        
        :param in_progress: Is the SIP registration is still in progress or not? 
        :type in_progress: bool
        
        :param status_code: The list of SIP response codes. The __code1:code2__ means a range from __code1__ to __code2__ including; the __code1;code2__ meanse either __code1__ or __code2__. You can combine ranges, e.g., __code1;code2:code3__. 
        :type status_code: str
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_sip_registration_type(p)
        return res

    def attach_phone_number(self, country_code, phone_category_name, phone_region_id, phone_count=None, phone_number=None, country_state=None, regulation_address_id=None):
        """
        Attach the phone number to the account. To attach the German, Italian phone numbers you should specify the phone_owner_* parameters.

        
        :param country_code: The country code. 
        :type country_code: str
        
        :param phone_category_name: The phone category name. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbercategories'>GetPhoneNumberCategories</a> method. 
        :type phone_category_name: str
        
        :param phone_region_id: The phone region ID. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumberregionsb'>GetPhoneNumberRegions</a> method. 
        :type phone_region_id: int
        
        :param phone_count: The phone count to attach. 
        :type phone_count: int
        
        :param phone_number: The phone number that can be used instead of <b>phone_count</b>. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbers'>GetNewPhoneNumbers</a> method. 
        :type phone_number: str
        
        :param country_state: The country state. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbercategories'>GetPhoneNumberCategories</a> and <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbercountrystates'>GetPhoneNumberCountryStates</a> methods. 
        :type country_state: str
        
        :param regulation_address_id: The phone regulation address ID. 
        :type regulation_address_id: int
        
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
            params['phone_number']=phone_number

        if country_state is not None:
            params['country_state']=country_state

        if regulation_address_id is not None:
            params['regulation_address_id']=regulation_address_id

        
        res = self._perform_request('AttachPhoneNumber', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def bind_phone_number_to_application(self, phone_id=None, phone_number=None, application_id=None, application_name=None, rule_id=None, rule_name=None, bind=None):
        """
        Bind the phone number to the application or unbind the phone number from the application. You should specify the application_id or application_name if you specify the rule_name.

        
        :param phone_id: The phone ID list or the 'all' value. 
        :type phone_id: list | int | string
        
        :param phone_number: The phone number list that can be used instead of <b>phone_id</b>. 
        :type phone_number: list | string
        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param application_name: The application name that can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param rule_id: The rule ID. 
        :type rule_id: int
        
        :param rule_name: The rule name that can be used instead of <b>rule_id</b>. 
        :type rule_name: str
        
        :param bind: Bind or unbind? 
        :type bind: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def deactivate_phone_number(self, phone_id=None, phone_number=None):
        """
        Deactivates the phone number.

        
        :param phone_id: The phone ID. 
        :type phone_id: int
        
        :param phone_number: The phone number that can be used instead of <b>phone_id</b>. 
        :type phone_number: str
        
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
            params['phone_id']=phone_id

        if phone_number is not None:
            params['phone_number']=phone_number

        
        res = self._perform_request('DeactivatePhoneNumber', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_phone_number_info(self, auto_charge, phone_id=None, phone_number=None):
        """
        Configure the phone number.

        
        :param auto_charge: Set true to enable the auto charging. 
        :type auto_charge: bool
        
        :param phone_id: The phone ID list or the 'all' value. 
        :type phone_id: list | int | string
        
        :param phone_number: The phone number list that can be used instead of <b>phone_id</b>. 
        :type phone_number: list | string
        
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
        
        
        params['auto_charge']=auto_charge

        
        if phone_id is not None:
            params['phone_id']=self._serialize_list(phone_id)

        if phone_number is not None:
            params['phone_number']=self._serialize_list(phone_number)

        
        res = self._perform_request('SetPhoneNumberInfo', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_phone_numbers(self, phone_id=None, application_id=None, application_name=None, is_bound_to_application=None, phone_template=None, country_code=None, phone_category_name=None, canceled=None, deactivated=None, auto_charge=None, from_phone_next_renewal=None, to_phone_next_renewal=None, from_phone_purchase_date=None, to_phone_purchase_date=None, child_account_id=None, children_phones_only=None, verification_name=None, verification_status=None, from_unverified_hold_until=None, to_unverified_hold_until=None, can_be_used=None, order_by=None, sandbox=None, count=None, offset=None, phone_region_name=None, rule_id=None, rule_name=None, is_bound_to_rule=None):
        """
        Gets the account phone numbers.

        
        :param phone_id: The particular phone ID to filter 
        :type phone_id: int
        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param application_name: The application name that can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param is_bound_to_application: Is a phone bound to an application. 
        :type is_bound_to_application: bool
        
        :param phone_template: The phone number start to filter 
        :type phone_template: str
        
        :param country_code: The country code list. 
        :type country_code: list | string
        
        :param phone_category_name: The phone category name. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbercategories'>GetPhoneNumberCategories</a> method. 
        :type phone_category_name: str
        
        :param canceled: The flag of the canceled (deleted) subscription to filter. 
        :type canceled: bool
        
        :param deactivated: The flag of the deactivated (frozen) subscription to filter. 
        :type deactivated: bool
        
        :param auto_charge: The auto_charge flag to filter. 
        :type auto_charge: bool
        
        :param from_phone_next_renewal: The UTC 'from' date filter in format: YYYY-MM-DD 
        :type from_phone_next_renewal: datetime.date
        
        :param to_phone_next_renewal: The UTC 'to' date filter in format: YYYY-MM-DD 
        :type to_phone_next_renewal: datetime.date
        
        :param from_phone_purchase_date: The UTC 'from' date filter in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type from_phone_purchase_date: datetime.datetime
        
        :param to_phone_purchase_date: The UTC 'to' date filter in 24-h format: YYYY-MM-DD HH:mm:ss 
        :type to_phone_purchase_date: datetime.datetime
        
        :param child_account_id: The child account ID list or the 'all' value. 
        :type child_account_id: list | int | string
        
        :param children_phones_only: Set true to get the children phones only. 
        :type children_phones_only: bool
        
        :param verification_name: The required account verification name to filter. 
        :type verification_name: str
        
        :param verification_status: The account verification status list. The following values are possible: REQUIRED, IN_PROGRESS, VERIFIED 
        :type verification_status: list | string
        
        :param from_unverified_hold_until: Unverified phone hold until the date (from ...) in format: YYYY-MM-DD 
        :type from_unverified_hold_until: datetime.date
        
        :param to_unverified_hold_until: Unverified phone hold until the date (... to) in format: YYYY-MM-DD 
        :type to_unverified_hold_until: datetime.date
        
        :param can_be_used: Can the unverified account use the phone? 
        :type can_be_used: bool
        
        :param order_by: The following values are available: 'phone_number' (ascent order), 'phone_price' (ascent order), 'phone_country_code' (ascent order), 'deactivated' (deactivated first, active last), 'purchase_date' (descent order), 'phone_next_renewal' (ascent order), 'verification_status', 'unverified_hold_until' (ascent order), 'verification_name'. 
        :type order_by: str
        
        :param sandbox: Flag allows you to display only the numbers of the sandbox, real numbers, or all numbers. The following values are possible: 'all', 'true', 'false'. 
        :type sandbox: str
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :param phone_region_name: The region names list. 
        :type phone_region_name: list | string
        
        :param rule_id: The rule ID list. 
        :type rule_id: list | int | string
        
        :param rule_name: The rule names list. Can be used only if __application_id__ or __application_name__ is specified. 
        :type rule_name: list | string
        
        :param is_bound_to_rule: Is a number bound to any rule? 
        :type is_bound_to_rule: bool
        
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
            params['phone_id']=phone_id

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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_attached_phone_info_type(p)
        return res

    def get_new_phone_numbers(self, country_code, phone_category_name, phone_region_id, country_state=None, count=None, offset=None):
        """
        Gets the new phone numbers.

        
        :param country_code: The country code. 
        :type country_code: str
        
        :param phone_category_name: The phone category name. See the GetPhoneNumberCategories function. 
        :type phone_category_name: str
        
        :param phone_region_id: The phone region ID. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumberregions'>GetPhoneNumberRegions</a> method. 
        :type phone_region_id: int
        
        :param country_state: The country state. See the GetPhoneNumberCategories and GetPhoneNumberCountryStates functions. 
        :type country_state: str
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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

        
        res = self._perform_request('GetNewPhoneNumbers', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_new_phone_info_type(p)
        return res

    def get_phone_number_categories(self, country_code=None, sandbox=None):
        """
        Gets the phone number categories.

        
        :param country_code: The country code. 
        :type country_code: str
        
        :param sandbox: Flag allows you to display phone number categories only of the sandbox, real or all .The following values are possible: 'all', 'true', 'false'. 
        :type sandbox: str
        
        :rtype: dict
        """
        params = dict()
        
        
        if country_code is not None:
            params['country_code']=country_code

        if sandbox is not None:
            params['sandbox']=sandbox

        
        res = self._perform_request('GetPhoneNumberCategories', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_phone_number_country_info_type(p)
        return res

    def get_phone_number_country_states(self, country_code, phone_category_name, country_state=None):
        """
        Gets the phone number country states.

        
        :param country_code: The country code. 
        :type country_code: str
        
        :param phone_category_name: The phone category name. See the GetPhoneNumberCategories function. 
        :type phone_category_name: str
        
        :param country_state: The country state code (example: AL, CA, ... ). 
        :type country_state: str
        
        :rtype: dict
        """
        params = dict()
        
        params['country_code']=country_code

        params['phone_category_name']=phone_category_name

        
        if country_state is not None:
            params['country_state']=country_state

        
        res = self._perform_request('GetPhoneNumberCountryStates', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_phone_number_country_state_info_type(p)
        return res

    def get_phone_number_regions(self, country_code, phone_category_name, country_state=None, omit_empty=None, phone_region_id=None, phone_region_name=None, phone_region_code=None):
        """
        Get the country regions of the phone numbers. The response will also contain the info about multiple numbers subscription for the child accounts.

        
        :param country_code: The country code. 
        :type country_code: str
        
        :param phone_category_name: The phone category name. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbercategories'>GetPhoneNumberCategories</a> method. 
        :type phone_category_name: str
        
        :param country_state: The country state code (example: AL, CA, ... ). 
        :type country_state: str
        
        :param omit_empty: Set to 'false' to show all the regions (with and without phone numbers in stock). 
        :type omit_empty: bool
        
        :param phone_region_id: The phone region ID to filter. 
        :type phone_region_id: int
        
        :param phone_region_name: The phone region name to filter. 
        :type phone_region_name: str
        
        :param phone_region_code: The region phone prefix to filter. 
        :type phone_region_code: str
        
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

        
        res = self._perform_request('GetPhoneNumberRegions', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_phone_number_country_region_info_type(p)
        return res

    def get_actual_phone_number_region(self, country_code, phone_category_name, phone_region_id):
        """
        Get actual info the country region of the phone numbers. The response will also contain the info about multiple numbers subscription for the child accounts.

        
        :param country_code: The country code. 
        :type country_code: str
        
        :param phone_category_name: The phone category name. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbercategoriesb'>GetPhoneNumberCategories</a> method. 
        :type phone_category_name: str
        
        :param phone_region_id: The phone region ID to filter. 
        :type phone_region_id: int
        
        :rtype: dict
        """
        params = dict()
        
        params['country_code']=country_code

        params['phone_category_name']=phone_category_name

        params['phone_region_id']=phone_region_id

        
        
        res = self._perform_request('GetActualPhoneNumberRegion', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
                self._preprocess_phone_number_country_region_info_type(res["result"])
        return res

    def add_caller_id(self, callerid_number):
        """
        Adds a new caller ID. Caller ID is the phone that will be displayed to the called user. This number can be used for call back.

        
        :param callerid_number: The callerID number in E.164 format. 
        :type callerid_number: str
        
        :rtype: dict
        """
        params = dict()
        
        params['callerid_number']=callerid_number

        
        
        res = self._perform_request('AddCallerID', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def activate_caller_id(self, verification_code, callerid_id=None, callerid_number=None):
        """
        Activates the CallerID by the verification code.

        
        :param verification_code: The verification code, see the VerifyCallerID function. 
        :type verification_code: str
        
        :param callerid_id: The id of the callerID object. 
        :type callerid_id: int
        
        :param callerid_number: The callerID number that can be used instead of <b>callerid_id</b>. 
        :type callerid_number: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_caller_id(self, callerid_id=None, callerid_number=None):
        """
        Deletes the CallerID. Note: you can't delete a CID permanently (the antispam defence).

        
        :param callerid_id: The id of the callerID object. 
        :type callerid_id: int
        
        :param callerid_number: The callerID number that can be used instead of <b>callerid_id</b>. 
        :type callerid_number: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_caller_ids(self, callerid_id=None, callerid_number=None, active=None, order_by=None, count=None, offset=None):
        """
        Gets the account callerIDs.

        
        :param callerid_id: The id of the callerID object to filter. 
        :type callerid_id: int
        
        :param callerid_number: The phone number to filter. 
        :type callerid_number: str
        
        :param active: The active flag to filter. 
        :type active: bool
        
        :param order_by: The following values are available: 'caller_number' (ascent order), 'verified_until' (ascent order). 
        :type order_by: str
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_caller_id_info_type(p)
        return res

    def verify_caller_id(self, callerid_id=None, callerid_number=None):
        """
        Gets a verification code by make call to the callerID number.

        
        :param callerid_id: The id of the callerID object. 
        :type callerid_id: int
        
        :param callerid_number: The callerID number that can be used instead of <b>callerid_id</b>. 
        :type callerid_number: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def add_queue(self, acd_queue_name, application_id=None, application_name=None, acd_queue_priority=None, auto_binding=None, service_probability=None, max_queue_size=None, max_waiting_time=None, average_service_time=None):
        """
        Adds a new ACD queue.

        
        :param acd_queue_name: The queue name. The length must be less than 100. 
        :type acd_queue_name: str
        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param application_name: The application name that can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param acd_queue_priority: The integer queue priority. The highest priority is 0. 
        :type acd_queue_priority: int
        
        :param auto_binding: Set false to disable the auto binding of operators to a queue by skills comparing. 
        :type auto_binding: bool
        
        :param service_probability: The value in the range of [0.5 ... 1.0]. The value 1.0 means the service probability 100% in challenge with a lower priority queue. 
        :type service_probability: int
        
        :param max_queue_size: The max queue size. 
        :type max_queue_size: int
        
        :param max_waiting_time: The max predicted waiting time in minutes. The client is rejected if the predicted waiting time is greater than the max predicted waiting time. 
        :type max_waiting_time: int
        
        :param average_service_time: The average service time in seconds. Specify the parameter to correct or initialize the waiting time prediction. 
        :type average_service_time: int
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def bind_user_to_queue(self, bind, application_id=None, application_name=None, user_id=None, user_name=None, acd_queue_id=None, acd_queue_name=None):
        """
        Bind/unbind users to/from the specified ACD queues. Note that users and queues should be already bound to the same application.

        
        :param bind: Bind or unbind users. 
        :type bind: bool
        
        :param application_id: The application ID. 
        :type application_id: int
        
        :param application_name: The application name that can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param user_id: The user ID list or the 'all' value to specify all users bound to the application. 
        :type user_id: list | int | string
        
        :param user_name: The user name that can be used instead of <b>user_id</b>. The user name list. 
        :type user_name: list | string
        
        :param acd_queue_id: The ACD queue ID list or the 'all' value to specify all queues bound to the application. 
        :type acd_queue_id: list | int | string
        
        :param acd_queue_name: The queue name that can be used instead of <b>acd_queue_id</b>. The queue name list. 
        :type acd_queue_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_queue(self, acd_queue_id=None, acd_queue_name=None):
        """
        Deletes the ACD queue.

        
        :param acd_queue_id: The ACD queue ID list. 
        :type acd_queue_id: list | int | string
        
        :param acd_queue_name: The ACD queue name that can be used instead of <b>acd_queue_id</b>. The ACD queue name list. 
        :type acd_queue_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_queue_info(self, acd_queue_id=None, acd_queue_name=None, new_acd_queue_name=None, acd_queue_priority=None, auto_binding=None, service_probability=None, max_queue_size=None, max_waiting_time=None, average_service_time=None, application_id=None):
        """
        Edits the ACD queue.

        
        :param acd_queue_id: The ACD queue ID. 
        :type acd_queue_id: int
        
        :param acd_queue_name: The ACD queue name that can be used instead of <b>acd_queue_id</b>. 
        :type acd_queue_name: str
        
        :param new_acd_queue_name: The new queue name. The length must be less than 100. 
        :type new_acd_queue_name: str
        
        :param acd_queue_priority: The integer queue priority. The highest priority is 0. 
        :type acd_queue_priority: int
        
        :param auto_binding: Set false to disable the auto binding of operators to a queue by skills comparing. 
        :type auto_binding: bool
        
        :param service_probability: The value in the range of [0.5 ... 1.0]. The value 1.0 means the service probability 100% in challenge with a lower priority queue. 
        :type service_probability: int
        
        :param max_queue_size: The max queue size. 
        :type max_queue_size: int
        
        :param max_waiting_time: The max predicted waiting time in minutes. The client is rejected if the predicted waiting time is greater than the max predicted waiting time. 
        :type max_waiting_time: int
        
        :param average_service_time: The average service time in seconds. Specify the parameter to correct or initialize the waiting time prediction. 
        :type average_service_time: int
        
        :param application_id: The new application ID. 
        :type application_id: int
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_queues(self, acd_queue_id=None, acd_queue_name=None, application_id=None, skill_id=None, excluded_skill_id=None, with_skills=None, showing_skill_id=None, count=None, offset=None):
        """
        Gets the ACD queues.

        
        :param acd_queue_id: The ACD queue ID to filter. 
        :type acd_queue_id: int
        
        :param acd_queue_name: The ACD queue name part to filter. 
        :type acd_queue_name: str
        
        :param application_id: The application ID to filter. 
        :type application_id: int
        
        :param skill_id: The skill ID to filter. 
        :type skill_id: int
        
        :param excluded_skill_id: The excluded skill ID to filter. 
        :type excluded_skill_id: int
        
        :param with_skills: Set true to get the bound skills. 
        :type with_skills: bool
        
        :param showing_skill_id: The skill to show in the 'skills' field output. 
        :type showing_skill_id: int
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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

        
        res = self._perform_request('GetQueues', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_queue_info_type(p)
        return res

    def get_acd_state(self, acd_queue_id=None):
        """
        Gets the current ACD queue state.

        
        :param acd_queue_id: The ACD queue ID list or the 'all' value. 
        :type acd_queue_id: list | int | string
        
        :rtype: dict
        """
        params = dict()
        
        
        if acd_queue_id is not None:
            params['acd_queue_id']=self._serialize_list(acd_queue_id)

        
        res = self._perform_request('GetACDState', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
                self._preprocess_acd_state_type(res["result"])
        return res

    def get_acd_operator_statistics(self, from_date, user_id, to_date=None, acd_queue_id=None, abbreviation=None, report=None, aggregation=None, group=None):
        """
        Get statistics for calls distributed to users (referred as 'operators') via the 'ACD' module. This method can filter statistic based on operator ids, queue ids and date-time interval. It can also group results by day or hour.

        
        :param from_date: Date and time of statistics interval begin. Time zone is UTC, format is 24-h 'YYYY-MM-DD HH:mm:ss' 
        :type from_date: datetime.datetime
        
        :param user_id: The user ID list or the 'all' value.  
        :type user_id: list | int | string
        
        :param to_date: Date and time of statistics interval begin. Time zone is UTC, format is 24-h 'YYYY-MM-DD HH:mm:ss' 
        :type to_date: datetime.datetime
        
        :param acd_queue_id: The ACD queue ID list or the 'all' value. 
        :type acd_queue_id: list | int | string
        
        :param abbreviation: If set to <b>true</b>, key names in returned JSON will be abbreviated to reduce response byte size. The abbreviations are: 'SA' for 'SpeedOfAnswer', 'HT' for 'HandlingTime', 'TT' for 'TalkTime', 'ACW' for 'AfterCallWork', 'TDT' for 'TotalDialingTime', 'THT' for 'TotalHandlingTime', 'TTT' for 'TotalTalkTime', 'TACW' for 'TotalAfterCallWork', 'AC' for 'AnsweredCalls', 'UAC' for 'UnansweredCalls' 
        :type abbreviation: bool
        
        :param report: List of item names abbreviations. Returned JSON will include keys only for the selected items. Special 'all' value defines all possible items, see [ACDOperatorStatisticsType] for a complete list. See 'abbreviation' description for complete abbreviation list 
        :type report: list | string
        
        :param aggregation: Specifies how records are grouped by date and time. If set to 'day', the criteria is a day number. If set to 'hour_of_day', the criteria is a 60-minute interval within a day. If set to 'hour', the criteria is both day number and 60-minute interval within that day. If set to 'none', records are not grouped by date and time 
        :type aggregation: str
        
        :param group: If set to 'user', first-level array in the resulting JSON will group records by the user ID, and second-level array will group them by date according to the 'aggregation' parameter. If set to 'aggregation', first-level array in the resulting JSON will group records according to the 'aggregation' parameter, and second-level array will group them by the user ID 
        :type group: str
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_acd_operator_aggregation_group_type(p)
        return res

    def get_acd_queue_statistics(self, from_date, to_date=None, abbreviation=None, acd_queue_id=None, report=None, aggregation=None):
        """
        Get statistics for calls distributed to users (referred as 'operators') via the 'queue' distribution system. This method can filter statistic based on operator ids, queue ids and date-time interval. It can also group results by day or hour.

        
        :param from_date: Date and time of statistics interval begin. Time zone is UTC, format is 24-h 'YYYY-MM-DD HH:mm:ss' 
        :type from_date: datetime.datetime
        
        :param to_date: Date and time of statistics interval begin. Time zone is UTC, format is 24-h 'YYYY-MM-DD HH:mm:ss' 
        :type to_date: datetime.datetime
        
        :param abbreviation: If set to <b>true</b>, key names in returned JSON will be abbreviated to reduce response byte size. The abbreviations are: 'WT' for 'WaitingTime', 'SA' for 'SpeedOfAnswer', 'AT' is for 'AbandonmentTime', 'HT' is for 'HandlingTime', 'TT' is for 'TalkTime', 'ACW' is for 'AfterCallWork', 'QL' is for 'QueueLength', 'TC' is for 'TotalCalls', 'AC' is for 'AnsweredCalls', 'UAC' is for 'UnansweredCalls', 'RC' is for 'RejectedCalls', 'SL' is for 'ServiceLevel', 'TWT' is for 'TotalWaitingTime', 'TST' is for 'TotalSubmissionTime', 'TAT' is for 'TotalAbandonmentTime', 'THT' is for 'TotalHandlingTime', 'TTT' is for 'TotalTalkTime', 'TACW' is for 'TotalAfterCallWork' 
        :type abbreviation: bool
        
        :param acd_queue_id: The ACD queue ID list or the 'all' value. 
        :type acd_queue_id: list | int | string
        
        :param report: List of item names abbreviations. Returned JSON will include keys only for the selected items. Special 'all' value defines all possible items, see [ACDQueueStatisticsType] for a complete list. See 'abbreviation' description for complete abbreviation list 
        :type report: list | string
        
        :param aggregation: Specifies how records are grouped by date and time. If set to 'day', the criteria is a day number. If set to 'hour_of_day', the criteria is a 60-minute interval within a day. If set to 'hour', the criteria is both day number and 60-minute interval within that day. If set to 'none', records are not grouped by date and time 
        :type aggregation: str
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_acd_queue_statistics_type(p)
        return res

    def get_acd_operator_status_statistics(self, from_date, user_id, to_date=None, acd_status=None, aggregation=None, group=None):
        """
        Get statistics for the specified operators and ACD statuses. This method can filter statistics by operator ids and statuses. It can also group results by day/hour or users.

        
        :param from_date: Date and time of statistics interval begin. Time zone is UTC, format is 24-h 'YYYY-MM-DD HH:mm:ss' 
        :type from_date: datetime.datetime
        
        :param user_id: The user ID list or the 'all' value.  
        :type user_id: list | string
        
        :param to_date: Date and time of statistics interval begin. Time zone is UTC, format is 24-h 'YYYY-MM-DD HH:mm:ss' 
        :type to_date: datetime.datetime
        
        :param acd_status: The ACD status list. The following values are possible: OFFLINE, ONLINE, READY, BANNED, IN_SERVICE, AFTER_SERVICE, TIMEOUT, DND. 
        :type acd_status: list | string
        
        :param aggregation: Specifies how records are grouped by date and time. If set to 'day', the criteria is a day number. If set to 'hour_of_day', the criteria is a 60-minute interval within a day. If set to 'hour', the criteria is both day number and 60-minute interval within that day. If set to 'none', records are not grouped by date and time 
        :type aggregation: str
        
        :param group: If set to 'user', first-level array in the resulting JSON will group records by the user ID, and second-level array will group them by date according to the 'aggregation' parameter. If set to 'aggregation', first-level array in the resulting JSON will group records according to the 'aggregation' parameter, and second-level array will group them by the user ID 
        :type group: str
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_acd_operator_status_aggregation_group_type(p)
        return res

    def add_skill(self, skill_name):
        """
        Adds a new ACD operator skill.

        
        :param skill_name: The ACD operator skill name. The length must be less than 512. 
        :type skill_name: str
        
        :rtype: dict
        """
        params = dict()
        
        params['skill_name']=skill_name

        
        
        res = self._perform_request('AddSkill', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_skill(self, skill_id=None, skill_name=None):
        """
        Deletes the skill.

        
        :param skill_id: The skill ID. 
        :type skill_id: int
        
        :param skill_name: The skill name that can be used instead of <b>skill_id</b>. 
        :type skill_name: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_skill_info(self, new_skill_name, skill_id=None, skill_name=None):
        """
        Edits the skill.

        
        :param new_skill_name: The new skill name. The length must be less than 512. 
        :type new_skill_name: str
        
        :param skill_id: The skill ID. 
        :type skill_id: int
        
        :param skill_name: The skill name that can be used instead of <b>skill_id</b>. 
        :type skill_name: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_skills(self, skill_id=None, skill_name=None, count=None, offset=None):
        """
        Gets the skills.

        
        :param skill_id: The skill ID to filter. 
        :type skill_id: int
        
        :param skill_name: The skill name part to filter. 
        :type skill_name: str
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_skill_info_type(p)
        return res

    def bind_skill(self, skill_id=None, skill_name=None, user_id=None, user_name=None, acd_queue_id=None, acd_queue_name=None, application_id=None, application_name=None, bind=None):
        """
        Binds the specified skills to the users (ACD operators) and/or the ACD queues.

        
        :param skill_id: The skill ID list or the 'all' value. 
        :type skill_id: list | int | string
        
        :param skill_name: Can be used instead of <b>skill_id</b>. The skill name list. 
        :type skill_name: list | string
        
        :param user_id: The user ID list or the 'all' value. 
        :type user_id: list | int | string
        
        :param user_name: The user name that can be used instead of <b>user_id</b>. The user name list. 
        :type user_name: list | string
        
        :param acd_queue_id: The ACD queue ID list or the 'all' value. 
        :type acd_queue_id: list | int | string
        
        :param acd_queue_name: The ACD queue name that can be used instead of <b>acd_queue_id</b>. The ACD queue name list. 
        :type acd_queue_name: list | string
        
        :param application_id: The application ID. It is required if the <b>user_name</b> is specified. 
        :type application_id: int
        
        :param application_name: The application name that can be used instead of <b>application_id</b>. 
        :type application_name: str
        
        :param bind: Bind or unbind? 
        :type bind: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_account_documents(self, with_details=None, verification_name=None, verification_status=None, from_unverified_hold_until=None, to_unverified_hold_until=None, child_account_id=None, children_verifications_only=None):
        """
        Gets the account documents and the verification states.

        
        :param with_details: Set true to view the uploaded document statuses. (The flag is ignored with the child_account_id=all) 
        :type with_details: bool
        
        :param verification_name: The required account verification name to filter. 
        :type verification_name: str
        
        :param verification_status: The account verification status list. The following values are possible: REQUIRED, IN_PROGRESS, VERIFIED 
        :type verification_status: list | string
        
        :param from_unverified_hold_until: Unverified subscriptions hold until the date (from ...) in format: YYYY-MM-DD 
        :type from_unverified_hold_until: datetime.date
        
        :param to_unverified_hold_until: Unverified subscriptions hold until the date (... to) in format: YYYY-MM-DD 
        :type to_unverified_hold_until: datetime.date
        
        :param child_account_id: The child account ID list or the 'all' value. 
        :type child_account_id: list | int | string
        
        :param children_verifications_only: Set true to get the children account verifications only. 
        :type children_verifications_only: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_account_verifications(p)
        return res

    def add_admin_user(self, new_admin_user_name, admin_user_display_name, new_admin_user_password, admin_user_active=None, admin_role_id=None, admin_role_name=None):
        """
        Adds a new admin user into the specified parent or child account.

        
        :param new_admin_user_name: The admin user name. The length must be less than 50. 
        :type new_admin_user_name: str
        
        :param admin_user_display_name: The admin user display name. The length must be less than 256. 
        :type admin_user_display_name: str
        
        :param new_admin_user_password: The admin user password. The length must be at least 6 symbols. 
        :type new_admin_user_password: str
        
        :param admin_user_active: The admin user enable flag. 
        :type admin_user_active: bool
        
        :param admin_role_id: The role(s) ID created via <a href='//voximplant.com/docs/references/httpapi/managing_admin_roles'>Managing Admin Roles</a> methods. The attaching admin role ID list or the 'all' value. 
        :type admin_role_id: str
        
        :param admin_role_name: The role(s) name(s) created via <a href='//voximplant.com/docs/references/httpapi/managing_admin_roles'>Managing Admin Roles</a> methods. The attaching admin role name that can be used instead of <b>admin_role_id</b>. 
        :type admin_role_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_admin_user(self, required_admin_user_id=None, required_admin_user_name=None):
        """
        Deletes the specified admin user.

        
        :param required_admin_user_id: The admin user ID list or the 'all' value. 
        :type required_admin_user_id: list | int | string
        
        :param required_admin_user_name: The admin user name to delete, can be used instead of <b>required_admin_user_id</b>. 
        :type required_admin_user_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_admin_user_info(self, required_admin_user_id=None, required_admin_user_name=None, new_admin_user_name=None, admin_user_display_name=None, new_admin_user_password=None, admin_user_active=None):
        """
        Edits the specified admin user.

        
        :param required_admin_user_id: The admin user to edit. 
        :type required_admin_user_id: int
        
        :param required_admin_user_name: The admin user to edit, can be used instead of <b>required_admin_user_id</b>. 
        :type required_admin_user_name: str
        
        :param new_admin_user_name: The new admin user name. The length must be less than 50. 
        :type new_admin_user_name: str
        
        :param admin_user_display_name: The new admin user display name. The length must be less than 256. 
        :type admin_user_display_name: str
        
        :param new_admin_user_password: The new admin user password. The length must be at least 6 symbols. 
        :type new_admin_user_password: str
        
        :param admin_user_active: The admin user enable flag. 
        :type admin_user_active: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_admin_users(self, required_admin_user_id=None, required_admin_user_name=None, admin_user_display_name=None, admin_user_active=None, with_roles=None, with_access_entries=None, count=None, offset=None):
        """
        Gets the admin users of the specified account. Note that both account types - parent and child - could have its own admins.

        
        :param required_admin_user_id: The admin user ID to filter. 
        :type required_admin_user_id: int
        
        :param required_admin_user_name: The admin user name part to filter. 
        :type required_admin_user_name: str
        
        :param admin_user_display_name: The admin user display name part to filter. 
        :type admin_user_display_name: str
        
        :param admin_user_active: The admin user active flag to filter. 
        :type admin_user_active: bool
        
        :param with_roles: Set true to get the attached admin roles. 
        :type with_roles: bool
        
        :param with_access_entries: Set true to get the admin user permissions. 
        :type with_access_entries: bool
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_admin_user_type(p)
        return res

    def add_admin_role(self, admin_role_name, admin_role_active=None, like_admin_role_id=None, like_admin_role_name=None, allowed_entries=None, denied_entries=None):
        """
        Adds a new admin role.

        
        :param admin_role_name: The admin role name. The length must be less than 50. 
        :type admin_role_name: str
        
        :param admin_role_active: The admin role enable flag. If false the allowed and denied entries have no affect. 
        :type admin_role_active: bool
        
        :param like_admin_role_id: The admin role ID list or the 'all' value. The list specifies the roles from which the new role automatically copies all permissions (allowed_entries and denied_entries). 
        :type like_admin_role_id: list | int | string
        
        :param like_admin_role_name: The admin role name that can be used instead of <b>like_admin_role_id</b>. The name specifies a role from which the new role automatically copies all permissions (allowed_entries and denied_entries). 
        :type like_admin_role_name: list | string
        
        :param allowed_entries: The list of allowed access entries (the API function names). 
        :type allowed_entries: list | string
        
        :param denied_entries: The list of denied access entries (the API function names). 
        :type denied_entries: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_admin_role(self, admin_role_id=None, admin_role_name=None):
        """
        Deletes the specified admin role.

        
        :param admin_role_id: The admin role ID list or the 'all' value. 
        :type admin_role_id: list | int | string
        
        :param admin_role_name: The admin role name to delete, can be used instead of <b>admin_role_id</b>. 
        :type admin_role_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_admin_role_info(self, admin_role_id=None, admin_role_name=None, new_admin_role_name=None, admin_role_active=None, entry_modification_mode=None, allowed_entries=None, denied_entries=None, like_admin_role_id=None, like_admin_role_name=None):
        """
        Edits the specified admin role.

        
        :param admin_role_id: The admin role to edit. 
        :type admin_role_id: int
        
        :param admin_role_name: The admin role to edit, can be used instead of <b>admin_role_id</b>. 
        :type admin_role_name: str
        
        :param new_admin_role_name: The new admin role name. The length must be less than 50. 
        :type new_admin_role_name: str
        
        :param admin_role_active: The admin role enable flag. If false the allowed and denied entries have no affect. 
        :type admin_role_active: bool
        
        :param entry_modification_mode: The modification mode of the permission lists (allowed_entries and denied_entries). The following values are possible: add, del, set. 
        :type entry_modification_mode: str
        
        :param allowed_entries: The list of allowed access entry changes (the API function names). 
        :type allowed_entries: list | string
        
        :param denied_entries: The list of denied access entry changes (the API function names). 
        :type denied_entries: list | string
        
        :param like_admin_role_id: The admin role ID list or the 'all' value. The list specifies the roles from which the allowed_entries and denied_entries will be merged. 
        :type like_admin_role_id: list | int | string
        
        :param like_admin_role_name: The admin role name, can be used instead of <b>like_admin_role_id</b>. The name specifies a role from which the allowed_entries and denied_entries will be merged. 
        :type like_admin_role_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_admin_roles(self, admin_role_id=None, admin_role_name=None, admin_role_active=None, with_entries=None, with_account_roles=None, with_parent_roles=None, included_admin_user_id=None, excluded_admin_user_id=None, full_admin_users_matching=None, showing_admin_user_id=None, count=None, offset=None):
        """
        Gets the admin roles.

        
        :param admin_role_id: The admin role ID to filter. 
        :type admin_role_id: int
        
        :param admin_role_name: The admin role name part to filter. 
        :type admin_role_name: str
        
        :param admin_role_active: The admin role active flag to filter. 
        :type admin_role_active: bool
        
        :param with_entries: Set true to get the permissions. 
        :type with_entries: bool
        
        :param with_account_roles: Set false to omit the account roles. 
        :type with_account_roles: bool
        
        :param with_parent_roles: Set false to omit the parent roles. 
        :type with_parent_roles: bool
        
        :param included_admin_user_id: The attached admin user ID list or the 'all' value. 
        :type included_admin_user_id: list | int | string
        
        :param excluded_admin_user_id: The not attached admin user ID list or the 'all' value. 
        :type excluded_admin_user_id: list | int | string
        
        :param full_admin_users_matching: Set false to get roles with partial admin user list matching. 
        :type full_admin_users_matching: str
        
        :param showing_admin_user_id: The admin user to show in the 'admin_users' field output. 
        :type showing_admin_user_id: int
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_admin_role_type(p)
        return res

    def attach_admin_role(self, required_admin_user_id=None, required_admin_user_name=None, admin_role_id=None, admin_role_name=None, mode=None):
        """
        Attaches the admin role(s) to the already existing admin(s).

        
        :param required_admin_user_id: The admin user ID list or the 'all' value. 
        :type required_admin_user_id: list | int | string
        
        :param required_admin_user_name: The admin user name to bind, can be used instead of <b>required_admin_user_id</b>. 
        :type required_admin_user_name: list | string
        
        :param admin_role_id: The role(s) ID created via <a href='//voximplant.com/docs/references/httpapi/managing_admin_roles'>Managing Admin Roles</a> methods. The attached admin role ID list or the 'all' value. 
        :type admin_role_id: list | int | string
        
        :param admin_role_name: The role(s) name(s) created via <a href='//voximplant.com/docs/references/httpapi/managing_admin_roles'>Managing Admin Roles</a> methods. The admin role name to attach, can be used instead of <b>admin_role_id</b>. 
        :type admin_role_name: list | string
        
        :param mode: The merge mode. The following values are possible: add, del, set. 
        :type mode: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_available_admin_role_entries(self):
        """
        Gets the all available admin role entries.

        
        :rtype: dict
        """
        params = dict()
        
        
        
        res = self._perform_request('GetAvailableAdminRoleEntries', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def add_authorized_account_ip(self, authorized_ip, allowed=None):
        """
        Adds a new authorized IP4 or network to the white/black list.

        
        :param authorized_ip: The authorized IP4 or network. 
        :type authorized_ip: str
        
        :param allowed: Set false to add the IP to the blacklist. 
        :type allowed: bool
        
        :rtype: dict
        """
        params = dict()
        
        params['authorized_ip']=authorized_ip

        
        if allowed is not None:
            params['allowed']=allowed

        
        res = self._perform_request('AddAuthorizedAccountIP', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_authorized_account_ip(self, authorized_ip=None, contains_ip=None, allowed=None):
        """
        Removes the authorized IP4 or network from the white/black list.

        
        :param authorized_ip: The authorized IP4 or network to remove. Set to 'all' to remove all items. 
        :type authorized_ip: str
        
        :param contains_ip: Can be used instead of <b>autharized_ip</b>. Specify the parameter to remove the networks that contains the particular IP4. 
        :type contains_ip: str
        
        :param allowed: Set true to remove the network from the white list. Set false to remove the network from the black list. Omit the parameter to remove the network from all lists. 
        :type allowed: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_authorized_account_ips(self, authorized_ip=None, allowed=None, contains_ip=None, count=None, offset=None):
        """
        Gets the authorized IP4 or network.

        
        :param authorized_ip: The authorized IP4 or network to filter. 
        :type authorized_ip: str
        
        :param allowed: The allowed flag to filter. 
        :type allowed: bool
        
        :param contains_ip: Specify the parameter to filter the networks that contains the particular IP4. 
        :type contains_ip: str
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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

        
        res = self._perform_request('GetAuthorizedAccountIPs', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_authorized_account_ip_type(p)
        return res

    def check_authorized_account_ip(self, authorized_ip):
        """
        Tests whether the IP4 is banned or allowed.

        
        :param authorized_ip: The IP4 to test. 
        :type authorized_ip: str
        
        :rtype: dict
        """
        params = dict()
        
        params['authorized_ip']=authorized_ip

        
        
        res = self._perform_request('CheckAuthorizedAccountIP', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def linkregulation_address(self, regulation_address_id, phone_id=None, phone_number=None):
        """
        Link regulation address to phone

        
        :param regulation_address_id: The regulation address ID 
        :type regulation_address_id: int
        
        :param phone_id: The phone ID for link 
        :type phone_id: int
        
        :param phone_number: The phone number for link 
        :type phone_number: str
        
        :rtype: dict
        """
        params = dict()
        
        passed_args = []
        if phone_id is not None:
            passed_args.append('phone_id')
        if phone_number is not None:
            passed_args.append('phone_number')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into linkregulation_address")
        if len(passed_args) == 0:
            raise VoximplantException("None of phone_id, phone_number passed into linkregulation_address")
        
        
        params['regulation_address_id']=regulation_address_id

        
        if phone_id is not None:
            params['phone_id']=phone_id

        if phone_number is not None:
            params['phone_number']=phone_number

        
        res = self._perform_request('LinkregulationAddress', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_zip_codes(self, country_code, phone_region_code=None, count=None, offset=None):
        """
        Search available zip codes

        
        :param country_code: The country code according to the <b>ISO 3166-1 alpha-2</b>. 
        :type country_code: str
        
        :param phone_region_code: The phone region code 
        :type phone_region_code: str
        
        :param count: The max returning record count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_zip_code(p)
        return res

    def get_regulations_address(self, country_code=None, phone_category_name=None, phone_region_code=None, regulation_address_id=None, verified=None, in_progress=None):
        """
        Search user's regulation address

        
        :param country_code: The country code according to the <b>ISO 3166-1 alpha-2</b>. 
        :type country_code: str
        
        :param phone_category_name: The phone category name. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbercategories'>GetPhoneNumberCategories</a> method. 
        :type phone_category_name: str
        
        :param phone_region_code: The phone region code. See the <a href='//voximplant.com/docs/references/httpapi/managing_regulation_address#getregions'>GetRegions</a> method. 
        :type phone_region_code: str
        
        :param regulation_address_id: The regulation address ID. 
        :type regulation_address_id: int
        
        :param verified: Show only verified regulation address. 
        :type verified: bool
        
        :param in_progress: Show only in progress regulation address. 
        :type in_progress: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_regulation_address(p)
        return res

    def get_available_regulations(self, country_code, phone_category_name, phone_region_code=None):
        """
        Search available regulation for link

        
        :param country_code: The country code according to the <b>ISO 3166-1 alpha-2</b>. 
        :type country_code: str
        
        :param phone_category_name: The phone category name. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbercategories'>GetPhoneNumberCategories</a> method. 
        :type phone_category_name: str
        
        :param phone_region_code: The phone region code. See the <a href='//voximplant.com/docs/references/httpapi/managing_regulation_address#getregions'>GetRegions</a> method. 
        :type phone_region_code: str
        
        :rtype: dict
        """
        params = dict()
        
        params['country_code']=country_code

        params['phone_category_name']=phone_category_name

        
        if phone_region_code is not None:
            params['phone_region_code']=phone_region_code

        
        res = self._perform_request('GetAvailableRegulations', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_countries(self, country_code=None):
        """
        Get all countries

        
        :param country_code: The country code according to the <b>ISO 3166-1 alpha-2</b>. 
        :type country_code: str
        
        :rtype: dict
        """
        params = dict()
        
        
        if country_code is not None:
            params['country_code']=country_code

        
        res = self._perform_request('GetCountries', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_regulation_country(p)
        return res

    def get_regions(self, country_code, phone_category_name, city_name=None, count=None, offset=None):
        """
        Get available regions in country

        
        :param country_code: The country code according to the <b>ISO 3166-1 alpha-2</b>. 
        :type country_code: str
        
        :param phone_category_name: The phone category name. See the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbercategories'>GetPhoneNumberCategories</a> method. 
        :type phone_category_name: str
        
        :param city_name: The pattern of city's name 
        :type city_name: str
        
        :param count: The returned regions count. 
        :type count: int
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_regulation_region_record(p)
        return res

    def add_push_credential(self, push_provider_name=None, push_provider_id=None, external_app_name=None, credential_bundle=None, cert_content=None, cert_file_name=None, cert_password=None, is_dev_mode=None, sender_id=None, server_key=None):
        """
        Add push credentials

        
        :param push_provider_name: The push provider name. Available values: APPLE, APPLE_VOIP, GOOGLE. 
        :type push_provider_name: str
        
        :param push_provider_id: The push provider id. 
        :type push_provider_id: int
        
        :param external_app_name: The application name. 
        :type external_app_name: str
        
        :param credential_bundle: The bundle of Android/iOS application. 
        :type credential_bundle: str
        
        :param cert_content: Public and private keys in PKCS12 format. 
        :type cert_content: str
        
        :param cert_file_name: The parameter is required, when set 'cert_content' as POST body. 
        :type cert_file_name: str
        
        :param cert_password: The secret password for private key. 
        :type cert_password: str
        
        :param is_dev_mode: Set true for use this certificate in apple's sandbox environment 
        :type is_dev_mode: bool
        
        :param sender_id: The sender id, provided by Google. 
        :type sender_id: str
        
        :param server_key: The server key, provided by Google. 
        :type server_key: str
        
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
        if sender_id is not None:
            passed_args.append('sender_id')
        if server_key is not None:
            passed_args.append('server_key')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into add_push_credential")
        if len(passed_args) == 0:
            raise VoximplantException("None of sender_id, server_key passed into add_push_credential")
        
        
        
        if push_provider_name is not None:
            params['push_provider_name']=push_provider_name

        if push_provider_id is not None:
            params['push_provider_id']=push_provider_id

        if external_app_name is not None:
            params['external_app_name']=external_app_name

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

        if sender_id is not None:
            params['sender_id']=sender_id

        if server_key is not None:
            params['server_key']=server_key

        
        res = self._perform_request('AddPushCredential', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_push_credential(self, push_credential_id, external_app_name, cert_content=None, cert_password=None, is_dev_mode=None, sender_id=None, server_key=None):
        """
        Modify push credentials

        
        :param push_credential_id: The push credentials id. 
        :type push_credential_id: int
        
        :param external_app_name: The application name. 
        :type external_app_name: str
        
        :param cert_content: Public and private keys in PKCS12 format. 
        :type cert_content: str
        
        :param cert_password: The secret password for private key. 
        :type cert_password: str
        
        :param is_dev_mode: Set true for use this certificate in apple's sandbox environment 
        :type is_dev_mode: bool
        
        :param sender_id: The sender id, provided by Google. 
        :type sender_id: str
        
        :param server_key: The server key, provided by Google. 
        :type server_key: str
        
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
        if sender_id is not None:
            passed_args.append('sender_id')
        if server_key is not None:
            passed_args.append('server_key')
        
        if len(passed_args) > 1:
            raise VoximplantException(", ". join(passed_args) + " passed simultaneously into set_push_credential")
        if len(passed_args) == 0:
            raise VoximplantException("None of sender_id, server_key passed into set_push_credential")
        
        
        params['push_credential_id']=push_credential_id

        params['external_app_name']=external_app_name

        
        if cert_content is not None:
            params['cert_content']=cert_content

        if cert_password is not None:
            params['cert_password']=cert_password

        if is_dev_mode is not None:
            params['is_dev_mode']=is_dev_mode

        if sender_id is not None:
            params['sender_id']=sender_id

        if server_key is not None:
            params['server_key']=server_key

        
        res = self._perform_request('SetPushCredential', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_push_credential(self, push_credential_id):
        """
        Remove push credentials

        
        :param push_credential_id: The push credentials id. 
        :type push_credential_id: int
        
        :rtype: dict
        """
        params = dict()
        
        params['push_credential_id']=push_credential_id

        
        
        res = self._perform_request('DelPushCredential', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_push_credential(self, push_credential_id=None, push_provider_name=None, push_provider_id=None, application_name=None, application_id=None, external_app=None, with_cert=None):
        """
        Get push credentials

        
        :param push_credential_id: The push credentials id. 
        :type push_credential_id: int
        
        :param push_provider_name: The push provider name. Available values: APPLE, APPLE_VOIP, GOOGLE. 
        :type push_provider_name: str
        
        :param push_provider_id: The push provider id. 
        :type push_provider_id: int
        
        :param application_name: The name of bound application. 
        :type application_name: str
        
        :param application_id: The id of bound application. 
        :type application_id: int
        
        :param external_app: The push provider's application name. 
        :type external_app: str
        
        :param with_cert: Set true to get the user's certificate. 
        :type with_cert: bool
        
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

        if external_app is not None:
            params['external_app']=external_app

        if with_cert is not None:
            params['with_cert']=with_cert

        
        res = self._perform_request('GetPushCredential', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_push_credential_info(p)
        return res

    def bind_push_credential(self, push_credential_id, application_id, bind=None):
        """
        Bind push credentials to applications

        
        :param push_credential_id: The push credentials ID list. 
        :type push_credential_id: list | int | string
        
        :param application_id: The application ID list or the 'all' value. 
        :type application_id: list | int | string
        
        :param bind: Set to false for unbind. Default value is true. 
        :type bind: bool
        
        :rtype: dict
        """
        params = dict()
        
        params['push_credential_id']=self._serialize_list(push_credential_id)

        params['application_id']=self._serialize_list(application_id)

        
        if bind is not None:
            params['bind']=bind

        
        res = self._perform_request('BindPushCredential', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def add_dialogflow_key(self, json_credentials, external_app_name=None, description=None):
        """
        Add Dialogflow key

        
        :param json_credentials: Dialogflow credentials, provided by JWK (Json web key). 
        :type json_credentials: str
        
        :param external_app_name: The application name. 
        :type external_app_name: str
        
        :param description: The Dialogflow keys's description. 
        :type description: str
        
        :rtype: dict
        """
        params = dict()
        
        params['json_credentials']=json_credentials

        
        if external_app_name is not None:
            params['external_app_name']=external_app_name

        if description is not None:
            params['description']=description

        
        res = self._perform_request('AddDialogflowKey', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_dialogflow_key(self, dialogflow_key_id, description):
        """
        Edit Dialogflow key

        
        :param dialogflow_key_id: The Dialogflow key's ID. 
        :type dialogflow_key_id: int
        
        :param description: The Dialogflow keys's description. To clear previously set description leave the parameter blank or put whitespaces only. 
        :type description: str
        
        :rtype: dict
        """
        params = dict()
        
        params['dialogflow_key_id']=dialogflow_key_id

        params['description']=description

        
        
        res = self._perform_request('SetDialogflowKey', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_dialogflow_key(self, dialogflow_key_id):
        """
        Remove Dialogflow key

        
        :param dialogflow_key_id: The Dialogflow key's ID. 
        :type dialogflow_key_id: int
        
        :rtype: dict
        """
        params = dict()
        
        params['dialogflow_key_id']=dialogflow_key_id

        
        
        res = self._perform_request('DelDialogflowKey', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_dialogflow_keys(self, dialogflow_key_id=None, application_name=None, application_id=None, external_app=None):
        """
        Get Dialogflow keys

        
        :param dialogflow_key_id: The Dialogflow key's ID. 
        :type dialogflow_key_id: int
        
        :param application_name: The name of bound application. 
        :type application_name: str
        
        :param application_id: The id of bound application. 
        :type application_id: int
        
        :param external_app: The push provider's application name. 
        :type external_app: str
        
        :rtype: dict
        """
        params = dict()
        
        
        if dialogflow_key_id is not None:
            params['dialogflow_key_id']=dialogflow_key_id

        if application_name is not None:
            params['application_name']=application_name

        if application_id is not None:
            params['application_id']=application_id

        if external_app is not None:
            params['external_app']=external_app

        
        res = self._perform_request('GetDialogflowKeys', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_dialogflow_key_info(p)
        return res

    def bind_dialogflow_keys(self, dialogflow_key_id, application_id, bind=None):
        """
        Bind a Dialogflow key to the specified applications

        
        :param dialogflow_key_id: The Dialogflow key's ID  
        :type dialogflow_key_id: int
        
        :param application_id: The application ID list or the 'all' value. 
        :type application_id: list | int | string
        
        :param bind: Set to false to unbind. Default value is true. 
        :type bind: bool
        
        :rtype: dict
        """
        params = dict()
        
        params['dialogflow_key_id']=dialogflow_key_id

        params['application_id']=self._serialize_list(application_id)

        
        if bind is not None:
            params['bind']=bind

        
        res = self._perform_request('BindDialogflowKeys', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def send_sms_message(self, source, destination, sms_body):
        """
        Send SMS message between two phone numbers. The source phone number should be purchased from Voximplant and support SMS (which is indicated by the <b>is_sms_supported</b> property in the objects returned by the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbers'>/GetPhoneNumbers</a> HTTP API) and SMS should be enabled for it via the <a href='//voximplant.com/docs/references/httpapi/managing_sms#controlsms'>/ControlSms</a> HTTP API. SMS messages can be received via HTTP callbacks, see <a href='//voximplant.com/blog/http-api-callbacks'>this article</a> for details.

        
        :param source: The source phone number. 
        :type source: str
        
        :param destination: The destination phone number. 
        :type destination: str
        
        :param sms_body: The message text, up to 70 characters. The message of 71-140 characters is billed like 2 messages; the message of 141-210 characters is billed like 3 messages and so on. 
        :type sms_body: str
        
        :rtype: dict
        """
        params = dict()
        
        params['source']=source

        params['destination']=destination

        params['sms_body']=sms_body

        
        
        res = self._perform_request('SendSmsMessage', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def control_sms(self, phone_number, command):
        """
        Enable or disable SMS sending and receiving for the phone number. Can be used only for phone numbers with SMS support, which is indicated by the <b>is_sms_supported</b> property in the objects returned by the <a href='//voximplant.com/docs/references/httpapi/managing_phone_numbers#getphonenumbers'>/GetPhoneNumbers</a> HTTP API. Each inbound SMS message is billed according to the <a href='//voximplant.com/pricing'>pricing</a>. If enabled, SMS can be sent from this phone number using the <a href='//voximplant.com/docs/references/httpapi/managing_sms#sendsmsmessage'>/SendSmsMessage</a> HTTP API and received using the [InboundSmsCallback] property of the HTTP callback. See <a href='//voximplant.com/blog/http-api-callbacks'>this article</a> for HTTP callback details.

        
        :param phone_number: The phone number. 
        :type phone_number: str
        
        :param command: The SMS control command. The following values are possible: enable, disable. 
        :type command: str
        
        :rtype: dict
        """
        params = dict()
        
        params['phone_number']=phone_number

        params['command']=command

        
        
        res = self._perform_request('ControlSms', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_record_storages(self, record_storage_id=None, record_storage_name=None):
        """
        Get the record storages.

        
        :param record_storage_id: The record storage ID list. 
        :type record_storage_id: list | int | string
        
        :param record_storage_name: The record storage name list. 
        :type record_storage_name: list | string
        
        :rtype: dict
        """
        params = dict()
        
        
        if record_storage_id is not None:
            params['record_storage_id']=self._serialize_list(record_storage_id)

        if record_storage_name is not None:
            params['record_storage_name']=self._serialize_list(record_storage_name)

        
        res = self._perform_request('GetRecordStorages', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
                self._preprocess_record_storage_info_type(res["result"])
        return res

    def create_key(self, description=None, role_id=None, role_name=None):
        """
        Creates a public/private key pair. You can optionally specify one or more roles for the key, see [this article](https://voximplant.com/blog/service-accounts-introduction) for details.

        
        :param description: The key's description. 
        :type description: str
        
        :param role_id: The role ID list. Use it instead of **role_name**, but not combine with. 
        :type role_id: list | int | string
        
        :param role_name: The role name list. Use it instead of **role_id**, but not combine with. 
        :type role_name: list | string
        
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

        if role_id is not None:
            params['role_id']=self._serialize_list(role_id)

        if role_name is not None:
            params['role_name']=self._serialize_list(role_name)

        
        res = self._perform_request('CreateKey', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_key_info(p)
        return res

    def get_keys(self, key_id=None, with_roles=None, offset=None, count=None):
        """
        Gets key info of the specified account.

        
        :param key_id: The key's ID. 
        :type key_id: str
        
        :param with_roles: Show roles for the key. 
        :type with_roles: bool
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :param count: The max returning record count. 
        :type count: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_key_view(p)
        return res

    def update_key(self, key_id, description):
        """
        Updates info of the specified key.

        
        :param key_id: The key's ID 
        :type key_id: str
        
        :param description: The key's description. 
        :type description: str
        
        :rtype: dict
        """
        params = dict()
        
        params['key_id']=key_id

        params['description']=description

        
        
        res = self._perform_request('UpdateKey', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def delete_key(self, key_id):
        """
        Deletes the specified key.

        
        :param key_id: The key's ID. 
        :type key_id: str
        
        :rtype: dict
        """
        params = dict()
        
        params['key_id']=key_id

        
        
        res = self._perform_request('DeleteKey', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_key_roles(self, key_id, role_id=None, role_name=None):
        """
        Set roles for the specified key.

        
        :param key_id: The key's ID. 
        :type key_id: str
        
        :param role_id: The role id list. 
        :type role_id: list | int | string
        
        :param role_name: The role name list. 
        :type role_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_key_roles(self, key_id):
        """
        Gets roles of the specified key.

        
        :param key_id: The key's ID. 
        :type key_id: str
        
        :rtype: dict
        """
        params = dict()
        
        params['key_id']=key_id

        
        
        res = self._perform_request('GetKeyRoles', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_role_view(p)
        return res

    def remove_key_roles(self, key_id, role_id=None, role_name=None):
        """
        Removes the specified roles of a key.

        
        :param key_id: The key's ID. 
        :type key_id: str
        
        :param role_id: The role id list. 
        :type role_id: list | int | string
        
        :param role_name: The role name list. 
        :type role_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def add_sub_user(self, new_subuser_name, new_subuser_password, role_id=None, role_name=None, description=None):
        """
        Creates a subuser.

        
        :param new_subuser_name: Login of a new subuser, should be unique within the Voximplant account. The login specified is always converted to lowercase. 
        :type new_subuser_name: str
        
        :param new_subuser_password: Password of a new subuser, plain text. 
        :type new_subuser_password: str
        
        :param role_id: The role id list. 
        :type role_id: list | int | string
        
        :param role_name: The role name list. 
        :type role_name: list | string
        
        :param description: Description of a new subuser. 
        :type description: str
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
                self._preprocess_sub_user_id(res["result"])
        return res

    def get_sub_users(self, subuser_id=None, with_roles=None, offset=None, count=None):
        """
        Gets subusers.

        
        :param subuser_id: The subuser's ID. 
        :type subuser_id: int
        
        :param with_roles: Show subuser's roles 
        :type with_roles: bool
        
        :param offset: The first <b>N</b> records will be skipped in the output. 
        :type offset: int
        
        :param count: The max returning record count. 
        :type count: int
        
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
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_sub_user_view(p)
        return res

    def set_sub_user_info(self, subuser_id, old_subuser_password=None, new_subuser_password=None, description=None):
        """
        Edits a subuser.

        
        :param subuser_id: The subuser's ID. 
        :type subuser_id: int
        
        :param old_subuser_password: The subuser old password. It is required if __new_subuser_password__ is specified. 
        :type old_subuser_password: str
        
        :param new_subuser_password: The new user password. The length must be at least 6 symbols. 
        :type new_subuser_password: str
        
        :param description: The new subuser description. 
        :type description: str
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def del_sub_user(self, subuser_id):
        """
        Deletes a subuser.

        
        :param subuser_id: The subuser's ID. 
        :type subuser_id: int
        
        :rtype: dict
        """
        params = dict()
        
        params['subuser_id']=subuser_id

        
        
        res = self._perform_request('DelSubUser', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def set_sub_user_roles(self, subuser_id, role_id=None, role_name=None):
        """
        Adds the specified roles for a subuser.

        
        :param subuser_id: The subuser's ID. 
        :type subuser_id: int
        
        :param role_id: The role id list. 
        :type role_id: list | int | string
        
        :param role_name: The role name list. 
        :type role_name: list | string
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_sub_user_roles(self, subuser_id, with_expanded_roles=None):
        """
        Gets the subuser's roles.

        
        :param subuser_id: The subuser's ID. 
        :type subuser_id: int
        
        :param with_expanded_roles: Show expanded roles 
        :type with_expanded_roles: bool
        
        :rtype: dict
        """
        params = dict()
        
        params['subuser_id']=subuser_id

        
        if with_expanded_roles is not None:
            params['with_expanded_roles']=with_expanded_roles

        
        res = self._perform_request('GetSubUserRoles', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_role_view(p)
        return res

    def remove_sub_user_roles(self, subuser_id, role_id=None, role_name=None, force=None):
        """
        Removes the specified roles of a subuser.

        
        :param subuser_id: The subuser's ID. 
        :type subuser_id: int
        
        :param role_id: The role id list. 
        :type role_id: list | int | string
        
        :param role_name: The role name list. 
        :type role_name: list | string
        
        :param force: Remove roles from all subuser keys. 
        :type force: bool
        
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
            raise VoximplantException(res["error"]["msg"])
        
        return res

    def get_roles(self, group_name=None):
        """
        Gets all roles.

        
        :param group_name: The role group. 
        :type group_name: str
        
        :rtype: dict
        """
        params = dict()
        
        
        if group_name is not None:
            params['group_name']=group_name

        
        res = self._perform_request('GetRoles', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_role_view(p)
        return res

    def get_role_groups(self):
        """
        Gets role groups

        
        :rtype: dict
        """
        params = dict()
        
        
        
        res = self._perform_request('GetRoleGroups', params)
        if "error" in res:
            raise VoximplantException(res["error"]["msg"])
        if "result" in res:
            for p in res["result"]:
                self._preprocess_role_group_view(p)
        return res