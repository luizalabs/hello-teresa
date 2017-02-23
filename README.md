# Hello Teresa
A collection of `Hello World` ready to deploy on [teresa](https://github.com/luizalabs/teresa-api) PaaS.

## Deploy

Some information to get your application up and running on Kubernetes with Teresa.

### Port
Don't listen on a hardcoded port, but instead read the port from the environment variable `PORT`. For instance:

```go
port := os.Getenv("PORT")
if port == "" {
    port = "5000"
}
http.ListenAndServe(fmt.Sprintf(":%s", port), nil)
```

The deploy process will set this variable

### Procfile
According to [Heroku's docs](https://devcenter.heroku.com/articles/procfile):

```
A Procfile is a mechanism for declaring what commands are run by your application’s
dynos on the Heroku platform.
```

Teresa follows the same principle.
As an example, a Python application might have the following command on Procfile:

    web: gunicorn -b 0.0.0.0:$PORT -w 3 --pythonpath src myapp.wsgi


### Language detection
When you deploy an app using Teresa, you don't have to specify your application's language - it'll be automatically detected.

> This step it's based on [Heroku's build packs](https://devcenter.heroku.com/articles/buildpacks).

#### Golang
Teresa will detect your application as Golang if you're using one of theses depedencies managers:

- [govendor](https://github.com/kardianos/govendor)
- [glide](https://github.com/Masterminds/glide)
- [GB](https://getgb.io/)
- [Godep](https://github.com/tools/godep)

If you don't need to deal with third party libs you just need to drop a simple `vendor/vendor.json`
file in the root dir of your application, for instance:

```json
{
  "comment": "",
  "ignore": "test",
  "package": [],
  "rootPath": "github.com/luizalabs/hello-teresa"
}
```

#### Python
To deploy a Python application on Teresa a `requirements.txt` file must be present in the root dir
of your application.  
The version of Python runtime can be specified with a `runtime.txt` file in the root dir, for instance:

    $ cat runtime.txt
    python-3.6.0

#### NodeJS
Teresa will detect your application as NodeJS when the application has a `package.json` file in the root dir.  
If no _Procfile_ is present in the root directory of your application during the build step,
your web process will be started by running `npm start`, a script you can specify in _package.json_, for instance:

```json
  "scripts": {
    "start": "node server.js"
  },
```

### teresa.yaml
Some features can be configured in a file called `teresa.yaml` in the the root dir of application.

> Check a complete example [here](./golang-healthcheck-rolling-update/teresa.yaml)

#### Health Check
Kubernetes has two types of [health checks](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/),
the `Readiness` and the `Liveness`.

- **Readiness**: Based on the time of "boot" of application, the Kubernetes uses this configuration to know when container is ready to start accepting traffic.
- **Liveness**: Conventional health check, the Kubernetes uses this configuration to know when to restart a container.

You can set both (_readiness_ and _liveness_) for your application in section `healthCheck` of the _teresa.yaml_, for instance:

```yaml
healthCheck:
    liveness:
        path: /healthcheck/
        timeoutSeconds: 2
        initialDelaySeconds: 10
        periodSeconds: 5
        failureThreshold: 2
        successThreshold: 1
    readiness:
        path: /healthcheck/
        timeoutSeconds: 5
        initialDelaySeconds: 5
        periodSeconds: 5
        failureThreshold: 5
        successThreshold: 1
```

> Teresa only perform health check based on _HTTP GET request_.

- **path**: endpoint of application than health check should hit.
- **timeoutSeconds**: timeout to determine if the application is unhealthy.
- **initialDelaySeconds**: delay (in seconds) to start to perform the execution of health check.
- **periodSeconds**: delay between checks.
- **failureThreshold**: max failure tolerance before restart the container.
- **successThreshold**: min number of success to determina that container it's healthy.

Any code greater than or equeal to 200 and less than 400 indicates success.
Any other code indicates failure.

#### Rolling Update
Kubernetes has the [Rolling Update](https://kubernetes.io/docs/user-guide/deployments/#rolling-update-deployment) strategy to deal with deploys.
With this strategy you can specify the `max unavailable` and the `max surge` fields to control
the rolling update process.  
You can set both (_maxUnavailable_ and _maxSurge_) for the deploy of your application in section
`RollingUpdate` of the _teresa.yaml_, for instance:

```yaml
rollingUpdate:
    maxUnavailable: "30%"
    maxSurge: "2"
```

- **Max Unavailable**: Specifies the maximum number of pods can be unavailable during the update process.
- **Max Surge**: Specifies the maximyum number of pods can be created above the desired number of pods.

> This field can be an absolute number (e.g. "2") or a percentage (e.g. "30%").
