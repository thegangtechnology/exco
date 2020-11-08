# excel_comment_orm
[![Build Status](https://travis-ci.org/thegangtechnology/excel_comment_orm.svg?branch=master)](https://travis-ci.org/thegangtechnology/excel_comment_orm)
[![codecov](https://codecov.io/gh/thegangtechnology/excel_comment_orm/branch/master/graph/badge.svg?token=8BrjxREw2O)](https://codecov.io/gh/thegangtechnology/excel_comment_orm)
Put the description here.

# What it does

The package allows you to declare orm mapping right in the excel file in the comments
 then use it to extract data from other similar file.
 
An example of template is shown below.

![Template](notebooks/quickstart/template.png)

Dynamic Location, Validation, Assumptions, custom Parser are also supported.


# Installation

```
pip install excel_comment_orm
```

# Simple Usage

```
import exco
processor = exco.from_excel('./quickstart_template.xlsx')
result = processor.process_excel('./quickstart_data_file.xlsx')
print(result.to_dict())
```

See Also [Quick Start Notebook](notebooks/quickstart/0%20Quick%20Start.ipynb)

