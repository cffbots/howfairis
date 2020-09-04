import sys
import requests
import re


def has_license(owner, repo):
    url = "https://api.github.com/repos/{0}/{1}/license".format(owner, repo)

    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except requests.HTTPError:
        print("Did not see a license file")
        return False
    except Exception as err:
        print(f"Other error occurred: {err}")

    return True


def has_zenodo_badge(s):
    regex = r"!\[.*\]\(https://zenodo\.org/badge/DOI/10\.5281/zenodo" + \
            r"\.[0-9]*\.svg\)\]\(https://doi\.org/10\.5281/zenodo\.[0-9]*\)"
    return re.compile(regex).search(s) is not None


def has_open_repository(owner, repo):
    url = "https://api.github.com/repos/{0}/{1}".format(owner, repo)

    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except requests.HTTPError:
        print("Repository doesn't seem to be publicly accessible.")
        return False
    except Exception as err:
        print(f"Other error occurred: {err}")

    return True


class HowFairIsChecker:
    def __init__(self, url):
        assert url.startswith("https://github.com/"), \
            "url should start with https://github.com"
        self.url = url
        self.readme = None
        self.repository_is_compliant = None
        self.license_is_compliant = None
        self.registry_is_compliant = None
        self.citation_is_compliant = None
        self.checklist_is_compliant = None
        self.badge = None
        self.owner = None
        self.repo = None
        self.readme_filename = None
        self.branch = None

    def check_badge(self):

        compliance = [
            self.repository_is_compliant, self.license_is_compliant,
            self.registry_is_compliant, self.citation_is_compliant,
            self.checklist_is_compliant
        ]

        compliant_symbol = "%E2%97%8F"
        noncompliant_symbol = "%E2%97%8B"
        compliance_string = "%20%20".join([
            compliant_symbol if c is True else noncompliant_symbol
            for c in compliance
        ])
        score = compliance_string.count(compliant_symbol)
        if score in [0, 1]:
            color_string = "red"
        elif score in [2, 3, 4]:
            color_string = "orange"
        elif score == 5:
            color_string = "green"

        self.badge = "![fair-software.eu](https://img.shields.io" +\
                     "/badge/fair--software.eu-{0}-{1})" \
                     .format(compliance_string, color_string)

        if self.readme.find(self.badge) == -1:
            print("\nWhile searching through your README.md, I" +
                  " did not find the expected badge:\n" + self.badge + "\n")
            sys.exit(1)
        else:
            print("\nExpected badge is equal to the actual badge. " +
                  "It's all good.\n")
            sys.exit(0)

    def check_checklist(self):
        print("(5/5) checklist checks TODO")
        return self

    def check_citation(self):
        print("(4/5) citation checks")
        self.citation_is_compliant = has_zenodo_badge(self.readme)
        return self

    def check_license(self):
        print("(2/5) license checks")
        self.license_is_compliant = has_license(self.owner, self.repo)
        return self

    def check_registry(self):
        print("(3/5) registry checks TODO")
        return self

    def check_repository(self):
        print("(1/5) repository checks")
        self.repository_is_compliant = \
            has_open_repository(self.owner, self.repo)
        return self

    def deconstruct_url(self):
        self.owner, self.repo = self.url.replace("https://github.com/",
                                                 "").split("/")[:2]
        self.branch = "master"
        self.readme_filename = "README.md"
        return self

    def get_readme(self):
        # only github urls supported
        # only README.md supported

        raw_url = "https://raw.githubusercontent.com/" + \
                  "{0}/{1}/{2}/{3}".format(self.owner, self.repo,
                                           self.branch, self.readme_filename)
        try:
            response = requests.get(raw_url)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")

        self.readme = response.text
        return self


def main():
    print("Checking compliance with fair-software.eu...")

    if len(sys.argv) != 2:
        raise Exception("Expected exactly one argument, i.e. the URL for " +
                        "which GitHub repository to run the analysis.")

    url = sys.argv[1]
    print("Running for {0}".format(url))
    checker = HowFairIsChecker(url)
    checker.deconstruct_url()
    checker.get_readme()
    checker.check_repository()
    checker.check_license()
    checker.check_registry()
    checker.check_citation()
    checker.check_checklist()
    checker.check_badge()


if __name__ == "__main__":
    main()
