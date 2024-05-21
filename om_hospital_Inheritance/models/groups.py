from odoo import api, fields, models


class ResGroups(models.Model):
    _inherit = "res.groups"

    def get_application_groups(self, domain):
        group_id = self.env.ref('project.group_project_task_dependencies').id
        gr_id = self.env.ref('project.group_project_stages').id

        return super(ResGroups, self).get_application_groups(domain + [('id', 'not in', (group_id, gr_id))])
