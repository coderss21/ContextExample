# Running this example

Navigate into this directory (`library/apps/hello-world`).

## Prerequisites

Install the `peak-cli` tool with:

```
pip install git+https://github.com/PeakBI/peak-cli.git
```

Then find an API Key for your chosen tenant and set it as an environment variable with:

```
export API_KEY={your-key-here}
```

## Publishing an App

Next, run the following command to publish your App:

```
peak apps specs create app.yaml . namespace={your-tenant-name-here}
```

If your App published successfully you should see something like:

```json
{"id": "{your-app-spec-id}"}
```

## Deploying an App

You can now either head over to the platform and you should see your App listed in Library (simply hit 'deploy' and follow
the instructions as required), or you can deploy via command line with:

```
peak apps deployments create {your-app-spec-id} hello-world --notes="{...}"
```

You should get a deployment ID in response.

## Cleaning up

You can then list deployments with:

```
peak apps deployments list
```

And delete a deployment with:

```
peak apps deployments delete {your-deployment-id}
```

And that's it, you're good!

## Notes

At the time of writing (Sept '22):

* All deployments must have a unique name (i.e. you can't deploy `hello-world` twice: one can be `hello-world`, another must be `hello-world-2` etc.)
* All deployments must have revision notes. This may change in future but is currently mandatory.
* All names must be alphanumeric, and may contain hyphens and spaces.
* You can only publish an App into one tenant at a time. This will change in future.

### Gotchas

* Due to limitations of an underlying service, the `context` option for images in Workflow Blocks does not work as expected. This example shows a viable workaround. This is being worked on and will be fixed in a future release.
