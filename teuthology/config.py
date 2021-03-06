import os
import yaml
import logging

log = logging.getLogger(__name__)


class Config(object):
    """
    This class is intended to unify teuthology's many configuration files and
    objects. Currently it serves as a convenient interface to
    ~/.teuthology.yaml and nothing else.
    """
    teuthology_yaml = os.path.join(os.environ['HOME'], '.teuthology.yaml')
    defaults = {
        'archive_base': '/var/lib/teuthworker/archive',
        'ceph_git_base_url': 'https://github.com/ceph/',
        'lock_server': 'http://teuthology.front.sepia.ceph.com/locker/lock',
        'max_job_time': 259200,  # 3 days
        'results_server': 'http://paddles.front.sepia.ceph.com/',
        'results_email': 'ceph-qa@ceph.com',
        'verify_host_keys': True,
        'watchdog_interval': 600,
    }

    def __init__(self):
        self.load_files()

    def load_files(self):
        if os.path.exists(self.teuthology_yaml):
            self.__conf = yaml.safe_load(file(self.teuthology_yaml))
        else:
            log.debug("%s not found", self.teuthology_yaml)
            self.__conf = {}

    def __getattr__(self, name):
        return self.__conf.get(name, self.defaults.get(name))

    def __setattribute__(self, name, value):
        if name.endswith('__conf'):
            setattr(self, name, value)
        else:
            self.__conf[name] = value

config = Config()
