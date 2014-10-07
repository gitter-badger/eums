from django.db import models
from django.db.models import Q
from model_utils.fields import StatusField
from model_utils import Choices

from eums.models import DistributionPlanLineItem


class RunQueue(models.Model):
    STATUS = Choices('not_started', 'started')
    node_line_item = models.ForeignKey(DistributionPlanLineItem)
    contact_person_id = models.CharField(max_length=255)
    status = StatusField()
    run_delay = models.DecimalField(decimal_places=1, max_digits=12)

    class Meta:
        app_label = 'eums'

    @classmethod
    def enqueue(cls, node_line_item, run_delay):
        queued_run = RunQueue(node_line_item=node_line_item, status=RunQueue.STATUS.not_started,
                              contact_person_id=node_line_item.distribution_plan_node.consignee.contact_person_id,
                              run_delay=run_delay)
        queued_run.save()

    @classmethod
    def deque(cls, contact_person_id):
        not_started_runs = RunQueue.objects.filter(Q(contact_person_id=contact_person_id) & Q(status='not_started')).\
            order_by('-run_delay')
        if len(not_started_runs):
            return not_started_runs[0]
        return None