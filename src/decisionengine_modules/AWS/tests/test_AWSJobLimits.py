import os

import pandas as pd

from decisionengine.framework.modules.Module import verify_products
import decisionengine_modules.AWS.sources.AWSJobLimits as AWSJobLimits

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

config = {'data_file': os.path.join(DATA_DIR,
                                    'job_limits_sample.csv')}

expected_pandas_df = pd.read_csv(config.get("data_file")).drop_duplicates(subset=['AvailabilityZone', 'InstanceType'],
                                                                          keep='last').reset_index(drop=True)
produces = {'Job_Limits': pd.DataFrame}


class TestAWSJobLimits:

    def test_produces(self):
        aws_job_limits = AWSJobLimits.AWSJobLimits(config)
        assert aws_job_limits._produces == produces

    def test_acquire(self):
        aws_job_limits = AWSJobLimits.AWSJobLimits(config)
        res = aws_job_limits.acquire()
        verify_products(aws_job_limits, res)
        assert expected_pandas_df.equals(res.get('Job_Limits'))
