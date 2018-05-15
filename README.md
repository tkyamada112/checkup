# checkup

## Description

Detection Failure EC2 or RDS instances.
Assumed to be two envrironments. (DEV, PRD)

## Installation

```
pip install
```

## Usage

Edit `credentials.py` before execution.

```
# credentials
DEV_AWS_ACCESS_KEY_ID="xxx"
DEV_AWS_SECRET_ACCESS_KEY="xxx"
DEV_REGION="xxx"
PRD_AWS_ACCESS_KEY_ID="xxx"
PRD_AWS_SECRET_ACCESS_KEY="xxx"
PRD_REGION="xxx"
```

```
python checkup -env dev
python checkup -env prd
```

