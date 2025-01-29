from django_rq.management.commands.rqworker import Command as RQWorkerCommand


class Command(RQWorkerCommand):
    """
    A special worker command for Windows that always uses rq_win.WindowsWorker.
    """
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.set_defaults(worker_class='rq_win.WindowsWorker')
