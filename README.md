# Exco


[![Build Status](https://travis-ci.org/thegangtechnology/exco.svg?branch=master)](https://travis-ci.org/thegangtechnology/exco)
[![codecov](https://codecov.io/gh/thegangtechnology/exco/branch/master/graph/badge.svg?token=8BrjxREw2O)](https://codecov.io/gh/thegangtechnology/exco)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=thegangtechnology_exco&metric=alert_status)](https://sonarcloud.io/dashboard?id=thegangtechnology_exco)

Excel Comment ORM. Declare ORM Spec descriptively right on excel file.

# What it does

The package allows you to declare orm mapping right in the excel file in the comments
 then use it to extract data from other similar file.
 
An example of template is shown below.

![Template](notebooks/quickstart/template.png)

Dynamic Location, Validation, Assumptions, custom Parser are also supported.


# Installation

```
pip install exco
```

# Simple Usage

```
import exco
processor = exco.from_excel('./quickstart_template.xlsx')
result = processor.process_excel('./quickstart_data_file.xlsx')
print(result.to_dict())
```

See Also [Quick Start Notebook](notebooks/quickstart/0%20Quick%20Start.ipynb)

