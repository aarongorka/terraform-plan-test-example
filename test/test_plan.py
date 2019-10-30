#!/usr/bin/env python3
import os
import pytest
import json
from pprint import pprint


@pytest.fixture(scope="module")
def get_plan():
    with open("../terraform-plan.json") as fh:
        plan = json.loads(fh.read())
    yield plan


def test_not_wrong_statefile(get_plan):
    resource_changes = get_plan["resource_changes"]
    # return a list of every action taken in the plan
    list_of_lists = [resource_change['change']['actions'] for resource_change in resource_changes]
    # flatten list of lists
    pre_dedup_list = [val for sublist in list_of_lists for val in sublist]
    # make list of actions sorted and unique
    all_actions = list(sorted(set(pre_dedup_list)))
    print(all_actions)
    # if the only actions are create and delete (and no `noops`) then you're _probably_ operating on the wrong statefile
    assert(all_actions != ["create", "delete"])
