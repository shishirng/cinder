# Copyright (C) 2012 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Client side of the volume backup RPC API.
"""


from oslo_config import cfg
from oslo_log import log as logging
import oslo_messaging as messaging

from cinder import rpc
from cinder.api.metricutil import ReportMetrics

CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class BackupAPI(object):
    """Client side of the volume rpc API.

    API version history:

        1.0 - Initial version.
    """

    BASE_RPC_API_VERSION = '1.0'

    def __init__(self):
        super(BackupAPI, self).__init__()
        target = messaging.Target(topic=CONF.backup_topic,
                                  version=self.BASE_RPC_API_VERSION)
        self.client = rpc.get_client(target, '1.0')

    def _get_cctxt(self):
        return self.client.prepare()

    @ReportMetrics("backup-rpcapi-create-backup")
    def create_backup(self, ctxt, host, backup_id, volume_id, orig_status):
        LOG.debug("create_backup in rpcapi backup_id %s", backup_id)
        cctxt = self._get_cctxt()
        cctxt.cast(ctxt, 'create_backup', backup_id=backup_id,
                   orig_status=orig_status)

    @ReportMetrics("backup-rpcapi-restore-backup")
    def restore_backup(self, ctxt, host, backup_id, volume_id):
        LOG.debug("restore_backup in rpcapi backup_id %s", backup_id)
        cctxt = self._get_cctxt()
        cctxt.cast(ctxt, 'restore_backup', backup_id=backup_id,
                   volume_id=volume_id)

    @ReportMetrics("backup-rpcapi-delete-backup")
    def delete_backup(self, ctxt, host, backup_id):
        LOG.debug("delete_backup  rpcapi backup_id %s", backup_id)
        cctxt = self._get_cctxt()
        cctxt.cast(ctxt, 'delete_backup', backup_id=backup_id)

    def export_record(self, ctxt, host, backup_id):
        LOG.debug("export_record in rpcapi backup_id %(id)s "
                  "on host %(host)s.",
                  {'id': backup_id,
                   'host': host})
        cctxt = self._get_cctxt()
        return cctxt.call(ctxt, 'export_record', backup_id=backup_id)

    def import_record(self,
                      ctxt,
                      host,
                      backup_id,
                      backup_service,
                      backup_url,
                      backup_hosts):
        LOG.debug("import_record rpcapi backup id %(id)s "
                  "on host %(host)s for backup_url %(url)s.",
                  {'id': backup_id,
                   'host': host,
                   'url': backup_url})
        cctxt = self._get_cctxt()
        cctxt.cast(ctxt, 'import_record',
                   backup_id=backup_id,
                   backup_service=backup_service,
                   backup_url=backup_url,
                   backup_hosts=backup_hosts)

    def reset_status(self, ctxt, host, backup_id, status):
        LOG.debug("reset_status in rpcapi backup_id %(id)s "
                  "on host %(host)s.",
                  {'id': backup_id,
                   'host': host})
        cctxt = self._get_cctxt()
        return cctxt.cast(ctxt, 'reset_status', backup_id=backup_id,
                          status=status)
