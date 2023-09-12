## General concept

Looking for an overview of how Library fits together? Fortunately for you, [there is just such a document](https://docs.google.com/presentation/d/1a9ovm8u9P5Acu-ibsnRV2ygv3O_LuZS6Tnmuh9GE6OI/edit?usp=sharing).

## Prerequisites

To run this example, you'll need to be working in an environment with Python 3.9 or greater. You'll also need to install
the `peak-cli` package with:

```bash
pip install git+https://github.com/PeakBI/peak-cli.git
```

You can check the installation worked with:

```peak --help```

And should see something like:

```
Usage: peak [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  ...
  workflows  Workflows service
```

Note that this installation will allow you to interact programmatically with the `peak-cli` SDK via Python, too.

**This guide was written for the pre-release of Library API v1. Check you are using the correct version before 
proceeding.**

## Publishing your Workflow Spec

To publish your Workflow Block, you first need to publish your Workflow Spec. This contains all the instructions the 
Peak platform needs to provision the infrastructure and deploy the code in the Workflow you'd like to share. When you've
published this Spec, you'll be able to create multiple deployments from the same Spec. This means you can quickly deploy
many versions of the same Workflow Block onto a given tenant.

### Publish with CLI

To publish your Workflow Spec, navigate into this directory (`hello-world`) and then run the following command:

```bash
peak workflows specs create workflow.yaml .
```

You should see an output in your terminal similar to:

```json
{"id": "ddf089c6-a05e-4779-adc2-3fe4edb3f36e"}
```

To confirm your Workflow Spec has been published, run:

```bash
peak workflows specs list
```

You should see a list with at least one Spec with the above ID (`specId`).

### Publish with SDK

Alternatively you can publish via the SDK with:

```python
from peak.services.workflows import specs
specs.create("workflow.yaml", ".")
print(specs.ls())
```

## Creating a Workflow Deployment

Next, time to create a Deployment from your newly published Workflow Spec.

### Deploying via CLI

To create a Deployment, simply run:

```bash
peak workflows deployments create {specId}
```

Where the `{specId}` is the response from your publish request. You can run this command as many times as you like:
the Peak platform will create a unique Deployment for each request. Note that this will result in the creation of many
identical Workflows, and may incur significant cost if not used carefully.

You should see a response similar to:

```json
{
  "id": "db283fc2-9164-4027-b09e-8c1ecedb122b",
  "imageIds": [
    1
  ],
  "workflowId": 1
}
```

To confirm your Deployment was successfully created, run:

```bash
peak workflows deployments list
```

You should see your new deployment listed (see `specId` and `deploymentId`).

### Publish with SDK

Alternatively you can deploy via the SDK with:

```python
from peak.services.workflows import deployments

deployments.create(spec_id="db283fc2-9164-4027-b09e-8c1ecedb122b")
print(deployments.ls())
```

## Editing your Workflow

With your Workflow in service, the next question is: how do you update it?

To do this, you will need to either create a new Spec, or update the existing Spec, depending on your use-case. 
### Downloading the source code

The first step is to download your source code. To do this, run:

```bash
peak workflows specs list
```

For the spec you wish to edit, copy the `specId` and then run: 

```bash
peak artifacts download {specId} artifact.zip
```

This will download the Spec and it's bundled source code to your current directory as a compressed archive. Unzip the
artifact with:

```bash
unzip artifact.zip {your-project-name}
```

Where `{your-project-name}` is the name of the project (or the spec itself). The archive should decompress and you 
should see the source code inside the given directory.

You can now edit the source code freely. If you anticipate making lots of changes (especially over an extended period), 
you should make sure to initialise a `git` repo before continuing.

### Republishing your Workflow

With your changes made, it's time to republish your Spec and redeploy! Here you have two options...

#### Option A - Publishing a new release

Your first option is to update the existing Spec in-place. This is a great idea if you'd like to supersede the existing
Workflow with a bug fix or feature enhancement. **By doing this, all future deployments of this Workflow Spec will be 
pointing at your updated version by default.** Note that this _is_ limited by the namespace of your Spec (i.e. if your
namespace is your tenant, only future deployments of that Spec in that tenant will be affected).

Before publishing, **you must increment your release number**. This **must** be valid semantic versioning, and **must**
be of a higher increment than the preceding release.

```yaml
version: '1'
kind: 'workflow'
metadata:
  name: 'hello-world'
  release: '0.0.2'
  description: 'A hello world workflow'
  namespace: 'acmeinc'
...
```

Next, you can submit your update with:

```bash
peak workflows specs update {specId} workflow.yaml .
```

To confirm the update, you can run:

```bash
peak workflows specs list
```

You should see that the `latestRelease` of your Spec now aligns to the one you've just published.

#### Option B - Publishing as a new Spec

Your second option is to publish a new Spec entirely. This is similar to forking the Spec. This is ideal if you'd like 
to create a Workflow with its own history - exactly what you'd want if you want to create a private version of a Spec, 
or if you want to experiment with some source code. In this case, **any changes you make to this Spec will not be 
pointed at by any future Deployments of the Spec**. You can make your changes freely, but make sure to assign your Spec
a new name, or alternatively choose a different `namespace` (`{metadata.namespace}.{metdata.name}` must always be 
unique).

```yaml
version: '1'
kind: 'workflow'
metadata:
  name: 'hello-world-2'
  release: '0.0.1'
  description: 'A new hello world workflow'
  namespace: 'acmeinc'
...
```

You should now run:

```bash
peak workflows specs create workflow.yaml .
```

To confirm the creation of your new Spec, you can run:

```bash
peak workflows specs list
```

You should see `hello-world-2` with the `acmeinc` `namespace`.

## Redeploy your Workflow

Finally, you can redeploy your Workflow. Note that this will create an entirely new Deployment. **Early versions of the Library 
framework do not support in-place updates for existing Deployments**. As before, simply run:

```bash
peak workflows deployments create {specId}
```

And that's it, you're done!