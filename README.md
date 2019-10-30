# Terraform Plan Test Example
Example for testing `terraform plan` output using not much more than Python and `json.loads()`.

The `test_not_wrong_statefile()` test asserts that your actions aren't solely `create` and `delete`. This probably indicates you've pointed your new project at someone else's statefile, causing all resources in the statefile to be deleted. A normal plan will have `update` and `noop`.

```bash
terraform plan -out terraform-plan.tfstate && terraform show -json terraform-plan.tfstate > terraform-plan.json
cd test/ && tox
```

Failure example output:
```text
test_plan.py::test_not_wrong_statefile ['create', 'delete']
FAILED

=================================== FAILURES ===================================
___________________________ test_not_wrong_statefile ___________________________

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
>       assert(all_actions != ["create", "delete"])
E       AssertionError: assert ['create', 'delete'] != ['create', 'delete']

test_plan.py:25: AssertionError
============================== 1 failed in 0.02s ===============================
```
