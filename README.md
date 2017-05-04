# ebs-auto-snapshot
Lambda function to take snapshot of EBS volume

***Lambda function configuration:***

- Runtime: Python 2.7
  
- Handler: index.handler
  
- Role: Create a lambda role with this inline policy
  
  ```
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Action": [
                  "lambda:InvokeFunction"
              ],
              "Resource": [
                  "*"
              ],
              "Effect": "Allow"
          },
          {
              "Action": [
                  "ec2:DeleteSnapshot",
                  "ec2:DescribeSnapshots",
                  "ec2:CreateSnapshot"
              ],
              "Resource": [
                  "*"
              ],
              "Effect": "Allow"
          }
      ]
   }
   ```
- Example payload (lambda test event):
```
{
  "volumeId":"vol-xxxxxxx",
  "description":"Root vol",
  "retentionDays":"7"
}
```

***EC2 configuration:***
- EC2 role: must include this policy: `lambda:InvokeFunction`
- Install CLI:
```
curl -O https://bootstrap.pypa.io/get-pip.py
apt-get install -qq python-dev
python2.7 get-pip.py
pip install --upgrade awscli
```

- Crontab entry: 
```
0 5 * * * /usr/local/bin/aws lambda invoke --region us-east-1 --function-name <lambda function arn> --payload '{"volumeId":"vol-xxxxxxxxxxx", "description":"Root Vol", "retentionDays":"14"}' output.txt
```
