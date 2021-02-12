import pytest
from howfairis import Platform
from howfairis import Repo
from tests.contracts.repo import Contract
from .mocker import mocker


@pytest.fixture
def mocked_repo(mocker):
    with mocker:
        return Repo("https://gitlab.com/jspaaks/badge-test")


class TestRepoNoArgs(Contract):

    def test_api(self, mocked_repo):
        assert mocked_repo.api == "https://gitlab.com/api/v4/projects/jspaaks%2Fbadge-test"

    def test_branch(self, mocked_repo):
        assert mocked_repo.branch is None

    def test_default_branch(self, mocked_repo):
        assert mocked_repo.default_branch == "master"

    def test_owner(self, mocked_repo):
        assert mocked_repo.owner == "jspaaks"

    def test_path(self, mocked_repo):
        assert mocked_repo.path == ""

    def test_platform(self, mocked_repo):
        assert mocked_repo.platform == Platform.GITLAB

    def test_raw_url_format_string(self, mocked_repo):
        assert mocked_repo.raw_url_format_string == "https://gitlab.com/jspaaks/badge-test/-/raw/master/{0}"

    def test_repo(self, mocked_repo):
        assert mocked_repo.repo == "badge-test"

    def test_url(self, mocked_repo):
        assert mocked_repo.url == "https://gitlab.com/jspaaks/badge-test"
