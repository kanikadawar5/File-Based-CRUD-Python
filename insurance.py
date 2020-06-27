import abc
import csv
import shutil
from _csv import writer
from abc import ABC
from tempfile import NamedTemporaryFile
from csv import writer

termInsuranceFilename = '/Users/b0213133/Projects/csrera/week5_dynamic_programming1/3_edit_distance/termins.csv'
lifeInsuranceFilename = '/Users/b0213133/Projects/csrera/week5_dynamic_programming1/3_edit_distance/termins.csv'
healthInsuranceFilename = '/Users/b0213133/Projects/csrera/week5_dynamic_programming1/3_edit_distance/termins.csv'
clientInsurancesFilename = '/Users/b0213133/Projects/csrera/week5_dynamic_programming1/3_edit_distance/output.csv'

fields = ["InsID", "PolicyID", "Name", "Age", "Country", "Plan_Type", "Claim_Status"]
policyIDs = []


# /Users/b0213133/Projects/csrera/week5_dynamic_programming1/3_edit_distance/clientapp.csv
def read_csv(filename, flag):
    print("in read csv", filename)
    if flag == "claim":
        fields = ["PolicyID", "Name", "Amount"]
    else:
        fields = ["InsID", "PolicyID", "Name", "Age", "Country", "Plan_Type", "Claim_Status"]
    with open(filename, 'r', encoding='ascii') as policyfile:
        csv_reader = csv.DictReader(policyfile, delimiter=',', fieldnames=fields)
        last_InsID = 0
        for row in csv_reader:
            # print("row", row)
            for pos in range(3):
                if flag == "claim":
                    flds = ["PolicyID", "Name", "Amount"]
                    print(pos, flds[pos], row[flds[pos]])
                    policyIDs.append(row['PolicyID'])
                elif flag == "getting_ins":
                    last_InsID = row['InsID']
                    print(pos, fields[pos], row[fields[pos]])
                else:
                    print("row", row)
            policyIDs.append(last_InsID)
        return policyIDs


def append_client(client_insurance_application, flag, policyfilename):
    fields = ["InsID", "PolicyID", "Name", "Age", "Country", "Plan_Type", "Claim_Status"]

    filename = clientInsurancesFilename
    print(client_insurance_application[1], type(client_insurance_application[1]), len(client_insurance_application[0]))

    print("size", len(client_insurance_application[0]), client_insurance_application[0] == '')
    if flag == "buy" and client_insurance_application[0] == '':
        print("Policy already bought. It can be claimed")
    elif flag == "claim" and client_insurance_application[0] == '':
        print("Please buy the policy first, then provide policy ID with application")
    elif flag == "claim":
        print("claiming policy")

        tempfile = NamedTemporaryFile(mode='w', delete=False)
        policiesIDs = set(read_csv(policyfilename, flag))
        last_InsID = int(read_csv(filename, "getting_ins").pop())
        print("*****************",int(last_InsID))

        print("policies", policiesIDs, fields, filename)

        with open(filename, 'r', encoding='utf8') as csvfile, tempfile:
            print("file opened")
            reader = csv.DictReader(csvfile, delimiter=',', fieldnames=fields, quotechar='"')
            writer = csv.DictWriter(tempfile, delimiter=',', fieldnames=fields, quotechar='"')
            policyId = 0

            for row in reader:
                print("dfghjhgfdfghj", row)
                temprow = row
                # count += 1
                print("testing", client_insurance_application[1], row["PolicyID"])
                if row["PolicyID"] == client_insurance_application[1]:
                    policyId = row['PolicyID']
                    print("checking", row["Name"], client_insurance_application[1])
                    print('updating row', row)
                    for entry in range(len(client_insurance_application)):
                        print("entry", entry, row[fields[entry]], client_insurance_application[entry])
                        row[fields[entry]] = client_insurance_application[entry]
                        row = {"InsID": last_InsID + 1, "PolicyID": row['PolicyID'], "Name": row['Name'], "Age": row['Age'],
                               "Country": row['Country'],
                               "Plan_Type": row['Plan_Type'], "Claim_Status": row['Claim_Status']}
                        # row.insert(0,'\n')
                # if count == data_count and policyId not in policiesIDs:
                #     print("Policy Id incorrect")
                #     row = temprow
                # elif row['Claim_Status'] != 1:
                #     print("Send 1 in claim status to claim")
                #     row = temprow
                print(row)
                writer.writerow(row)

        shutil.move(tempfile.name, filename)
    else:
        print("buying policy")
        with open(filename, 'a+', newline='', encoding='utf8') as write_obj:
            # Create a writer object from csv module
            dict_writer = csv.DictWriter(write_obj, fieldnames=fields)
            # Add dictionary as wor in the csv
            dict_of_elem = {}
            for entry in range(len(client_insurance_application)):
                print(client_insurance_application[entry], fields[entry])
                dict_of_elem[fields[entry]] = client_insurance_application[entry]
            print(dict_of_elem)
            dict_writer.writerow(dict_of_elem)
        # with open(filename, 'a') as write_obj:
        #     print("opnedd")
        #     writer = csv.writer(write_obj, delimiter=',', quotechar='"')
        #     writer.writerow(client_insurance_application)
        #     write_obj.close()


class Insurance(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def view_policy(self):
        pass

    def buy_policy(self, client_application_file):
        pass

    def apply_for_claim(self, client_application_file):
        pass


class TermInsurance(Insurance, ABC):
    def __init__(self, termInsuranceFilename):
        self.termInsuranceFilename = termInsuranceFilename

    def view_policy(self):
        read_csv(self.termInsuranceFilename, "")
        pass

    def buy_policy(self, client_application):
        flag = "buy"
        print("buying policy", client_application)
        append_client(client_application, flag, termInsuranceFilename)
        print("Bought policy")
        pass

    def apply_for_claim(self, client_application):
        print("claiming policy", client_application)
        append_client(client_application, flag="claim", policyfilename=termInsuranceFilename)
        pass


class LifeInsurance(Insurance, ABC):

    def __init__(self, lifeInsuranceFilename):
        self.termInsuranceFilename = lifeInsuranceFilename


    def view_policy(self, client_application):
        read_csv(self.lifeInsuranceFilename, "")
        pass

    def buy_policy(self, client_application):
        flag = "buy"
        print("buying policy", client_application)
        append_client(client_application, flag, lifeInsuranceFilename)
        print("Bought policy")
        pass

    def apply_for_claim(self, client_application):
        print("claiming policy", client_application)
        append_client(client_application, flag="claim", policyfilename=termInsuranceFilename)
        pass


class HealthInsurance(Insurance, ABC):

    def __init__(self, healthInsuranceFilename):
        self.termInsuranceFilename = lifeInsuranceFilename


    def view_policy(self, client_application):
        read_csv(self.healthInsuranceFilename, "")
        pass

    def buy_policy(self, client_application):
        flag = "buy"
        print("buying policy", client_application)
        append_client(client_application, flag, lifeInsuranceFilename)
        print("Bought policy")
        pass

    def apply_for_claim(self, client_application):
        print("claiming policy", client_application)
        append_client(client_application, flag="claim", policyfilename=healthInsuranceFilename)
        pass


# Call the insurance classes as under
def main():
    def read_input_csv(filename):
        print("reading csv", filename)
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            # line_count = 0
            for row in csv_reader:
                policy_id = row[0]
                client_name = row[1]
                client_age = row[2]
                client_country = row[3]
                plan_type = row[4]
                claim_status = row[
                                   5] or 0  # by default 0, indicating only bought, not claimed, changed to 1, when claimed
                print("Inputs from file are as - ", policy_id, client_name, client_age, client_country, plan_type,
                      claim_status)
                return [policy_id, client_name, client_age, client_country, plan_type, claim_status]
            # print(f'Processed {line_count} lines.')

    def action_to_be_performed(action_selected):
        switcher = {
            1: "view_policy",
            2: 'buy_policy',
            3: 'apply_for_claim',
        }
        return switcher.get(action_selected, "Invalid")

    def selecting_insurance(action_selected):
        print("Enter 1 for Term Insurance, 2 for Life Insurance and 3 for Health Insurance")
        insurance_type = int(input())
        insurance_types = {
            1: "TermInsurance",
            2: "LifeInsurance",
            3: "HealthInsurance",
        }
        insurance_details_files = {
            1: "termInsuranceFilename",
            2: "lifeInsuranceFilename",
            3: "healthInsuranceFilename",
        }
        action = action_to_be_performed(action_selected=action_selected)
        insurance = (eval(insurance_types[insurance_type]))(eval(insurance_details_files[insurance_type]))

        print("testing", insurance, "action_selected", action_selected, "action", action)
        if action_selected in [2, 3]:
            print("Enter client application csv file path")
            filename = str(input())
            client_insurance_application = read_input_csv(filename=filename)
            print("application", client_insurance_application)
            getattr(insurance, action)(client_insurance_application)
        else:
            getattr(insurance, action)()

    print("1. View policy 2. Buy Policy 3. Apply For Claim - Enter from [1, 2, 3]")
    option_selected = int(input())
    selecting_insurance(option_selected)


main()
