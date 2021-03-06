from decisionengine.framework.modules import Publisher
from decisionengine_modules.htcondor.publishers import publisher


@publisher.HTCondorManifests.consumes_dataframes('glideclientglobal_manifests')
class GlideClientGlobalManifests(publisher.HTCondorManifests):

    def __init__(self, config):
        super().__init__(config)
        self.classad_type = 'glideclientglobal'


    def create_invalidate_constraint(self, dataframe):
        for collector_host, group in dataframe.groupby(['CollectorHost']):
            client_names = list(set(group['ClientName']))
            client_names.sort()
            if client_names:
                constraint = '(glideinmytype == "%s") && (stringlistmember(ClientName, "%s"))' % (self.classad_type, ','.join(client_names))
                self.invalidate_ads_constraint[collector_host] = constraint


Publisher.describe(GlideClientGlobalManifests)
