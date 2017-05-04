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
