class ChecklistMixin:

    def check_checklist(self):
        force_state = self.force_checklist
        if force_state not in [True, False, None]:
            raise ValueError("Unexpected configuration value for force_checklist.")
        if isinstance(force_state, bool):
            print("(5/5) checklist: force {0}".format(force_state))
            return force_state
        print("(5/5) checklist")
        results = [
            self.has_core_infrastructures_badge(),
        ]
        return True in results

    def has_core_infrastructures_badge(self):
        regexes = [r"https://bestpractices\.coreinfrastructure\.org/projects/[0-9]*/badge"]
        return self._eval_regexes(regexes)
