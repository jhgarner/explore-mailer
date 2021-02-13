# explore-mailer
Automatic CSCI 101 Explore project presentation feedback emailer.

_Author:_ Kevin Barnard ([kbarnard@mymail.mines.edu](mailto:kbarnard@mymail.mines.edu))

---
#### Table of Contents
1. [Configuration](#1-configuration)
2. [Data munging](#2-data-munging)
3. [Template file](#3-template-file)
4. [_Parameters file (optional)_](#4-_parameters-file-optional_)
5. [Generate digest](#5-generate-digest)
6. [Send emails](#6-send-emails)
---
## Usage
### 1. Configuration
First, set the configuration parameters in `config.ini`.

_Example:_
```ini
[user]
email=jdoe@mymail.mines.edu
key=N!2mvOhPU?Y^T)
```

The `key` field is your MyMail IMAP/POP password, available at [identity.mines.edu](https://identity.mines.edu/), under `Manage Account`. This field field is ***not*** your Mines Multipass password. 

_Less secure app access_ (see [support.google.com/accounts/answer/6010255](https://support.google.com/accounts/answer/6010255)) must be turned **on** for this application to work. 

### 2. Data munging
Next, munge the available data into the correct file format.
Fundamentally, the format is a JSON-serialized list of objects with the following schema. 

_Note: An example is provided in `data/feedback_example.json`._

#### Feedback object schema
Each feedback object represents a single response to the feedback form. It conforms to the structure
```
{
  "recipient": {
    "first": [first],
    "last": [last],
    "email": [email]
  },
  "responses": {
    [key_1]: [val_1],
    [key_2]: [val_2],
    ...
    [key_n]: [val_n]
  }
}
```
with fields
- `first`: Recipient first name
- `last`: Recipient last name
- `email`: Recipient email address
- `key_{i}`: The `i`th key (i.e. one question on the form)
- `val_{i}`: The `i`th value (i.e. the response to that question)

Key-value pairs not present in **every** feedback object in a file will be omitted.

#### Feedback file
The feedback file is simply a JSON-serialized list of feedback objects:
```
[
  [object_1],
  [object_2],
  ...
  [object_n]
]
```

### 3. Template file
**explore-mailer** uses a template message file to generate the subject and body of each message.
This allows for keyword parameters (see next section) to be used.

The template file has the following format. The first line is the subject of the message, and the remaining lines constitute the body. Keyword parameters are specified in `{` `}`.

The only required keyword parameter is `{feedback}`, which is where the generated feedback table will be placed.

_Note: An example is provided in `templates/template_example.txt`_

```text
[subject]
[body_line_1]
[body_line_2]
...
[body_line_n]
```

Optional parameters may provided in the parameters file can be inserted as `{option}`.

### 4. _Parameters file (optional)_
If you would like to add keyword parameters to the template file, you must specify them in a JSON parameters file. This is simply a file containing a JSON-serialized object of key-value pairs.

Using the reserved keys `first`, `last`, `email`, or `feedback` will result in an overwrite of your specified value.

_Note: An example is provided in `parameters/parameters_example.json`_

### 5. Generate digest
Run `python generate.py [-o output_file] [-p parameters_file] [feedback_file] [template_file]`. 
This will generate a digest file `digest.json` (or whatever specified with `-o`) to be used in the next step.

_Example:_

```shell
> python generate.py -o digest_example.json \
                     -p parameters/parameters_example.json \
                     feedback/feedback_example.json \
                     templates/template_example_with_params.txt
```

### 6. Send emails
Once a digest file has been created (see steps 2-4), the emails can be sent by running `python send.py [digest_file]`.

_Example:_
```shell
> python send.py digest.json
```

A log file will be generated and saved to `logs/[digest_file].log`.
