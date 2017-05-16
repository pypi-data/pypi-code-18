# coding=utf-8
#####################################################
# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT #
#####################################################
# noqa: E128,E201
from .asyncclient import AsyncBaseClient
from .asyncclient import createApiClient
from .asyncclient import config
from .asyncclient import createTemporaryCredentials
from .asyncclient import createSession
_defaultConfig = config


class Queue(AsyncBaseClient):
    """
    The queue, typically available at `queue.taskcluster.net`, is responsible
    for accepting tasks and track their state as they are executed by
    workers. In order ensure they are eventually resolved.

    This document describes the API end-points offered by the queue. These
    end-points targets the following audience:
     * Schedulers, who create tasks to be executed,
     * Workers, who execute tasks, and
     * Tools, that wants to inspect the state of a task.
    """

    classOptions = {
        "baseUrl": "https://queue.taskcluster.net/v1"
    }

    async def task(self, *args, **kwargs):
        """
        Get Task Definition

        This end-point will return the task-definition. Notice that the task
        definition may have been modified by queue, if an optional property is
        not specified the queue may provide a default value.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["task"], *args, **kwargs)

    async def status(self, *args, **kwargs):
        """
        Get task status

        Get task status structure from `taskId`

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-status-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["status"], *args, **kwargs)

    async def listTaskGroup(self, *args, **kwargs):
        """
        List Task Group

        List tasks sharing the same `taskGroupId`.

        As a task-group may contain an unbounded number of tasks, this end-point
        may return a `continuationToken`. To continue listing tasks you must call
        the `listTaskGroup` again with the `continuationToken` as the
        query-string option `continuationToken`.

        By default this end-point will try to return up to 1000 members in one
        request. But it **may return less**, even if more tasks are available.
        It may also return a `continuationToken` even though there are no more
        results. However, you can only be sure to have seen all results if you
        keep calling `listTaskGroup` with the last `continuationToken` until you
        get a result without a `continuationToken`.

        If you are not interested in listing all the members at once, you may
        use the query-string option `limit` to return fewer.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/list-task-group-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["listTaskGroup"], *args, **kwargs)

    async def listDependentTasks(self, *args, **kwargs):
        """
        List Dependent Tasks

        List tasks that depend on the given `taskId`.

        As many tasks from different task-groups may dependent on a single tasks,
        this end-point may return a `continuationToken`. To continue listing
        tasks you must call `listDependentTasks` again with the
        `continuationToken` as the query-string option `continuationToken`.

        By default this end-point will try to return up to 1000 tasks in one
        request. But it **may return less**, even if more tasks are available.
        It may also return a `continuationToken` even though there are no more
        results. However, you can only be sure to have seen all results if you
        keep calling `listDependentTasks` with the last `continuationToken` until
        you get a result without a `continuationToken`.

        If you are not interested in listing all the tasks at once, you may
        use the query-string option `limit` to return fewer.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/list-dependent-tasks-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["listDependentTasks"], *args, **kwargs)

    async def createTask(self, *args, **kwargs):
        """
        Create New Task

        Create a new task, this is an **idempotent** operation, so repeat it if
        you get an internal server error or network connection is dropped.

        **Task `deadline´**, the deadline property can be no more than 5 days
        into the future. This is to limit the amount of pending tasks not being
        taken care of. Ideally, you should use a much shorter deadline.

        **Task expiration**, the `expires` property must be greater than the
        task `deadline`. If not provided it will default to `deadline` + one
        year. Notice, that artifacts created by task must expire before the task.

        **Task specific routing-keys**, using the `task.routes` property you may
        define task specific routing-keys. If a task has a task specific
        routing-key: `<route>`, then when the AMQP message about the task is
        published, the message will be CC'ed with the routing-key:
        `route.<route>`. This is useful if you want another component to listen
        for completed tasks you have posted.  The caller must have scope
        `queue:route:<route>` for each route.

        **Dependencies**, any tasks referenced in `task.dependencies` must have
        already been created at the time of this call.

        **Important** Any scopes the task requires are also required for creating
        the task. Please see the Request Payload (Task Definition) for details.

        This method takes input: ``http://schemas.taskcluster.net/queue/v1/create-task-request.json#``

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-status-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["createTask"], *args, **kwargs)

    async def defineTask(self, *args, **kwargs):
        """
        Define Task

        **Deprecated**, this is the same as `createTask` with a **self-dependency**.
        This is only present for legacy.

        This method takes input: ``http://schemas.taskcluster.net/queue/v1/create-task-request.json#``

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-status-response.json#``

        This method is ``deprecated``
        """

        return await self._makeApiCall(self.funcinfo["defineTask"], *args, **kwargs)

    async def scheduleTask(self, *args, **kwargs):
        """
        Schedule Defined Task

        scheduleTask will schedule a task to be executed, even if it has
        unresolved dependencies. A task would otherwise only be scheduled if
        its dependencies were resolved.

        This is useful if you have defined a task that depends on itself or on
        some other task that has not been resolved, but you wish the task to be
        scheduled immediately.

        This will announce the task as pending and workers will be allowed to
        claim it and resolve the task.

        **Note** this operation is **idempotent** and will not fail or complain
        if called with a `taskId` that is already scheduled, or even resolved.
        To reschedule a task previously resolved, use `rerunTask`.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-status-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["scheduleTask"], *args, **kwargs)

    async def rerunTask(self, *args, **kwargs):
        """
        Rerun a Resolved Task

        This method _reruns_ a previously resolved task, even if it was
        _completed_. This is useful if your task completes unsuccessfully, and
        you just want to run it from scratch again. This will also reset the
        number of `retries` allowed.

        Remember that `retries` in the task status counts the number of runs that
        the queue have started because the worker stopped responding, for example
        because a spot node died.

        **Remark** this operation is idempotent, if you try to rerun a task that
        is not either `failed` or `completed`, this operation will just return
        the current task status.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-status-response.json#``

        This method is ``deprecated``
        """

        return await self._makeApiCall(self.funcinfo["rerunTask"], *args, **kwargs)

    async def cancelTask(self, *args, **kwargs):
        """
        Cancel Task

        This method will cancel a task that is either `unscheduled`, `pending` or
        `running`. It will resolve the current run as `exception` with
        `reasonResolved` set to `canceled`. If the task isn't scheduled yet, ie.
        it doesn't have any runs, an initial run will be added and resolved as
        described above. Hence, after canceling a task, it cannot be scheduled
        with `queue.scheduleTask`, but a new run can be created with
        `queue.rerun`. These semantics is equivalent to calling
        `queue.scheduleTask` immediately followed by `queue.cancelTask`.

        **Remark** this operation is idempotent, if you try to cancel a task that
        isn't `unscheduled`, `pending` or `running`, this operation will just
        return the current task status.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-status-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["cancelTask"], *args, **kwargs)

    async def pollTaskUrls(self, *args, **kwargs):
        """
        Get Urls to Poll Pending Tasks

        Get a signed URLs to get and delete messages from azure queue.
        Once messages are polled from here, you can claim the referenced task
        with `claimTask`, and afterwards you should always delete the message.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/poll-task-urls-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["pollTaskUrls"], *args, **kwargs)

    async def claimWork(self, *args, **kwargs):
        """
        Claim Work

        Claim any task, more to be added later... long polling up to 20s.

        This method takes input: ``http://schemas.taskcluster.net/queue/v1/claim-work-request.json#``

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/claim-work-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["claimWork"], *args, **kwargs)

    async def claimTask(self, *args, **kwargs):
        """
        Claim Task

        claim a task, more to be added later...

        This method takes input: ``http://schemas.taskcluster.net/queue/v1/task-claim-request.json#``

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-claim-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["claimTask"], *args, **kwargs)

    async def reclaimTask(self, *args, **kwargs):
        """
        Reclaim task

        Refresh the claim for a specific `runId` for given `taskId`. This updates
        the `takenUntil` property and returns a new set of temporary credentials
        for performing requests on behalf of the task. These credentials should
        be used in-place of the credentials returned by `claimWork`.

        The `reclaimTask` requests serves to:
         * Postpone `takenUntil` preventing the queue from resolving
           `claim-expired`,
         * Refresh temporary credentials used for processing the task, and
         * Abort execution if the task/run have been resolved.

        If the `takenUntil` timestamp is exceeded the queue will resolve the run
        as _exception_ with reason `claim-expired`, and proceeded to retry to the
        task. This ensures that tasks are retried, even if workers disappear
        without warning.

        If the task is resolved, this end-point will return `409` reporting
        `RequestConflict`. This typically happens if the task have been canceled
        or the `task.deadline` have been exceeded. If reclaiming fails, workers
        should abort the task and forget about the given `runId`. There is no
        need to resolve the run or upload artifacts.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-reclaim-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["reclaimTask"], *args, **kwargs)

    async def reportCompleted(self, *args, **kwargs):
        """
        Report Run Completed

        Report a task completed, resolving the run as `completed`.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-status-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["reportCompleted"], *args, **kwargs)

    async def reportFailed(self, *args, **kwargs):
        """
        Report Run Failed

        Report a run failed, resolving the run as `failed`. Use this to resolve
        a run that failed because the task specific code behaved unexpectedly.
        For example the task exited non-zero, or didn't produce expected output.

        Do not use this if the task couldn't be run because if malformed
        payload, or other unexpected condition. In these cases we have a task
        exception, which should be reported with `reportException`.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-status-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["reportFailed"], *args, **kwargs)

    async def reportException(self, *args, **kwargs):
        """
        Report Task Exception

        Resolve a run as _exception_. Generally, you will want to report tasks as
        failed instead of exception. You should `reportException` if,

          * The `task.payload` is invalid,
          * Non-existent resources are referenced,
          * Declared actions cannot be executed due to unavailable resources,
          * The worker had to shutdown prematurely,
          * The worker experienced an unknown error, or,
          * The task explicitly requested a retry.

        Do not use this to signal that some user-specified code crashed for any
        reason specific to this code. If user-specific code hits a resource that
        is temporarily unavailable worker should report task _failed_.

        This method takes input: ``http://schemas.taskcluster.net/queue/v1/task-exception-request.json#``

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/task-status-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["reportException"], *args, **kwargs)

    async def createArtifact(self, *args, **kwargs):
        """
        Create Artifact

        This API end-point creates an artifact for a specific run of a task. This
        should **only** be used by a worker currently operating on this task, or
        from a process running within the task (ie. on the worker).

        All artifacts must specify when they `expires`, the queue will
        automatically take care of deleting artifacts past their
        expiration point. This features makes it feasible to upload large
        intermediate artifacts from data processing applications, as the
        artifacts can be set to expire a few days later.

        We currently support 4 different `storageType`s, each storage type have
        slightly different features and in some cases difference semantics.

        **S3 artifacts**, is useful for static files which will be stored on S3.
        When creating an S3 artifact the queue will return a pre-signed URL
        to which you can do a `PUT` request to upload your artifact. Note
        that `PUT` request **must** specify the `content-length` header and
        **must** give the `content-type` header the same value as in the request
        to `createArtifact`.

        **Azure artifacts**, are stored in _Azure Blob Storage_ service, which
        given the consistency guarantees and API interface offered by Azure is
        more suitable for artifacts that will be modified during the execution
        of the task. For example docker-worker has a feature that persists the
        task log to Azure Blob Storage every few seconds creating a somewhat
        live log. A request to create an Azure artifact will return a URL
        featuring a [Shared-Access-Signature](http://msdn.microsoft.com/en-us/library/azure/dn140256.aspx),
        refer to MSDN for further information on how to use these.
        **Warning: azure artifact is currently an experimental feature subject
        to changes and data-drops.**

        **Reference artifacts**, only consists of meta-data which the queue will
        store for you. These artifacts really only have a `url` property and
        when the artifact is requested the client will be redirect the URL
        provided with a `303` (See Other) redirect. Please note that we cannot
        delete artifacts you upload to other service, we can only delete the
        reference to the artifact, when it expires.

        **Error artifacts**, only consists of meta-data which the queue will
        store for you. These artifacts are only meant to indicate that you the
        worker or the task failed to generate a specific artifact, that you
        would otherwise have uploaded. For example docker-worker will upload an
        error artifact, if the file it was supposed to upload doesn't exists or
        turns out to be a directory. Clients requesting an error artifact will
        get a `403` (Forbidden) response. This is mainly designed to ensure that
        dependent tasks can distinguish between artifacts that were suppose to
        be generated and artifacts for which the name is misspelled.

        **Artifact immutability**, generally speaking you cannot overwrite an
        artifact when created. But if you repeat the request with the same
        properties the request will succeed as the operation is idempotent.
        This is useful if you need to refresh a signed URL while uploading.
        Do not abuse this to overwrite artifacts created by another entity!
        Such as worker-host overwriting artifact created by worker-code.

        As a special case the `url` property on _reference artifacts_ can be
        updated. You should only use this to update the `url` property for
        reference artifacts your process has created.

        This method takes input: ``http://schemas.taskcluster.net/queue/v1/post-artifact-request.json#``

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/post-artifact-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["createArtifact"], *args, **kwargs)

    async def getArtifact(self, *args, **kwargs):
        """
        Get Artifact from Run

        Get artifact by `<name>` from a specific run.

        **Public Artifacts**, in-order to get an artifact you need the scope
        `queue:get-artifact:<name>`, where `<name>` is the name of the artifact.
        But if the artifact `name` starts with `public/`, authentication and
        authorization is not necessary to fetch the artifact.

        **API Clients**, this method will redirect you to the artifact, if it is
        stored externally. Either way, the response may not be JSON. So API
        client users might want to generate a signed URL for this end-point and
        use that URL with a normal HTTP client.

        **Caching**, artifacts may be cached in data centers closer to the
        workers in-order to reduce bandwidth costs. This can lead to longer
        response times. Caching can be skipped by setting the header
        `x-taskcluster-skip-cache: true`, this should only be used for resources
        where request volume is known to be low, and caching not useful.
        (This feature may be disabled in the future, use is sparingly!)

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["getArtifact"], *args, **kwargs)

    async def getLatestArtifact(self, *args, **kwargs):
        """
        Get Artifact from Latest Run

        Get artifact by `<name>` from the last run of a task.

        **Public Artifacts**, in-order to get an artifact you need the scope
        `queue:get-artifact:<name>`, where `<name>` is the name of the artifact.
        But if the artifact `name` starts with `public/`, authentication and
        authorization is not necessary to fetch the artifact.

        **API Clients**, this method will redirect you to the artifact, if it is
        stored externally. Either way, the response may not be JSON. So API
        client users might want to generate a signed URL for this end-point and
        use that URL with a normal HTTP client.

        **Remark**, this end-point is slightly slower than
        `queue.getArtifact`, so consider that if you already know the `runId` of
        the latest run. Otherwise, just us the most convenient API end-point.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["getLatestArtifact"], *args, **kwargs)

    async def listArtifacts(self, *args, **kwargs):
        """
        Get Artifacts from Run

        Returns a list of artifacts and associated meta-data for a given run.

        As a task may have many artifacts paging may be necessary. If this
        end-point returns a `continuationToken`, you should call the end-point
        again with the `continuationToken` as the query-string option:
        `continuationToken`.

        By default this end-point will list up-to 1000 artifacts in a single page
        you may limit this with the query-string parameter `limit`.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/list-artifacts-response.json#``

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["listArtifacts"], *args, **kwargs)

    async def listLatestArtifacts(self, *args, **kwargs):
        """
        Get Artifacts from Latest Run

        Returns a list of artifacts and associated meta-data for the latest run
        from the given task.

        As a task may have many artifacts paging may be necessary. If this
        end-point returns a `continuationToken`, you should call the end-point
        again with the `continuationToken` as the query-string option:
        `continuationToken`.

        By default this end-point will list up-to 1000 artifacts in a single page
        you may limit this with the query-string parameter `limit`.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/list-artifacts-response.json#``

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["listLatestArtifacts"], *args, **kwargs)

    async def pendingTasks(self, *args, **kwargs):
        """
        Get Number of Pending Tasks

        Get an approximate number of pending tasks for the given `provisionerId`
        and `workerType`.

        The underlying Azure Storage Queues only promises to give us an estimate.
        Furthermore, we cache the result in memory for 20 seconds. So consumers
        should be no means expect this to be an accurate number.
        It is, however, a solid estimate of the number of pending tasks.

        This method takes output: ``http://schemas.taskcluster.net/queue/v1/pending-tasks-response.json#``

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["pendingTasks"], *args, **kwargs)

    async def ping(self, *args, **kwargs):
        """
        Ping Server

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["ping"], *args, **kwargs)

    funcinfo = {
        "cancelTask": {           'args': ['taskId'],
            'method': 'post',
            'name': 'cancelTask',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-status-response.json#',
            'route': '/task/<taskId>/cancel',
            'stability': 'stable'},
        "claimTask": {           'args': ['taskId', 'runId'],
            'input': 'http://schemas.taskcluster.net/queue/v1/task-claim-request.json#',
            'method': 'post',
            'name': 'claimTask',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-claim-response.json#',
            'route': '/task/<taskId>/runs/<runId>/claim',
            'stability': 'stable'},
        "claimWork": {           'args': ['provisionerId', 'workerType'],
            'input': 'http://schemas.taskcluster.net/queue/v1/claim-work-request.json#',
            'method': 'post',
            'name': 'claimWork',
            'output': 'http://schemas.taskcluster.net/queue/v1/claim-work-response.json#',
            'route': '/claim-work/<provisionerId>/<workerType>',
            'stability': 'stable'},
        "createArtifact": {           'args': ['taskId', 'runId', 'name'],
            'input': 'http://schemas.taskcluster.net/queue/v1/post-artifact-request.json#',
            'method': 'post',
            'name': 'createArtifact',
            'output': 'http://schemas.taskcluster.net/queue/v1/post-artifact-response.json#',
            'route': '/task/<taskId>/runs/<runId>/artifacts/<name>',
            'stability': 'stable'},
        "createTask": {           'args': ['taskId'],
            'input': 'http://schemas.taskcluster.net/queue/v1/create-task-request.json#',
            'method': 'put',
            'name': 'createTask',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-status-response.json#',
            'route': '/task/<taskId>',
            'stability': 'stable'},
        "defineTask": {           'args': ['taskId'],
            'input': 'http://schemas.taskcluster.net/queue/v1/create-task-request.json#',
            'method': 'post',
            'name': 'defineTask',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-status-response.json#',
            'route': '/task/<taskId>/define',
            'stability': 'deprecated'},
        "getArtifact": {           'args': ['taskId', 'runId', 'name'],
            'method': 'get',
            'name': 'getArtifact',
            'route': '/task/<taskId>/runs/<runId>/artifacts/<name>',
            'stability': 'stable'},
        "getLatestArtifact": {           'args': ['taskId', 'name'],
            'method': 'get',
            'name': 'getLatestArtifact',
            'route': '/task/<taskId>/artifacts/<name>',
            'stability': 'stable'},
        "listArtifacts": {           'args': ['taskId', 'runId'],
            'method': 'get',
            'name': 'listArtifacts',
            'output': 'http://schemas.taskcluster.net/queue/v1/list-artifacts-response.json#',
            'query': ['continuationToken', 'limit'],
            'route': '/task/<taskId>/runs/<runId>/artifacts',
            'stability': 'experimental'},
        "listDependentTasks": {           'args': ['taskId'],
            'method': 'get',
            'name': 'listDependentTasks',
            'output': 'http://schemas.taskcluster.net/queue/v1/list-dependent-tasks-response.json#',
            'query': ['continuationToken', 'limit'],
            'route': '/task/<taskId>/dependents',
            'stability': 'stable'},
        "listLatestArtifacts": {           'args': ['taskId'],
            'method': 'get',
            'name': 'listLatestArtifacts',
            'output': 'http://schemas.taskcluster.net/queue/v1/list-artifacts-response.json#',
            'query': ['continuationToken', 'limit'],
            'route': '/task/<taskId>/artifacts',
            'stability': 'experimental'},
        "listTaskGroup": {           'args': ['taskGroupId'],
            'method': 'get',
            'name': 'listTaskGroup',
            'output': 'http://schemas.taskcluster.net/queue/v1/list-task-group-response.json#',
            'query': ['continuationToken', 'limit'],
            'route': '/task-group/<taskGroupId>/list',
            'stability': 'stable'},
        "pendingTasks": {           'args': ['provisionerId', 'workerType'],
            'method': 'get',
            'name': 'pendingTasks',
            'output': 'http://schemas.taskcluster.net/queue/v1/pending-tasks-response.json#',
            'route': '/pending/<provisionerId>/<workerType>',
            'stability': 'stable'},
        "ping": {           'args': [],
            'method': 'get',
            'name': 'ping',
            'route': '/ping',
            'stability': 'stable'},
        "pollTaskUrls": {           'args': ['provisionerId', 'workerType'],
            'method': 'get',
            'name': 'pollTaskUrls',
            'output': 'http://schemas.taskcluster.net/queue/v1/poll-task-urls-response.json#',
            'route': '/poll-task-url/<provisionerId>/<workerType>',
            'stability': 'stable'},
        "reclaimTask": {           'args': ['taskId', 'runId'],
            'method': 'post',
            'name': 'reclaimTask',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-reclaim-response.json#',
            'route': '/task/<taskId>/runs/<runId>/reclaim',
            'stability': 'stable'},
        "reportCompleted": {           'args': ['taskId', 'runId'],
            'method': 'post',
            'name': 'reportCompleted',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-status-response.json#',
            'route': '/task/<taskId>/runs/<runId>/completed',
            'stability': 'stable'},
        "reportException": {           'args': ['taskId', 'runId'],
            'input': 'http://schemas.taskcluster.net/queue/v1/task-exception-request.json#',
            'method': 'post',
            'name': 'reportException',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-status-response.json#',
            'route': '/task/<taskId>/runs/<runId>/exception',
            'stability': 'stable'},
        "reportFailed": {           'args': ['taskId', 'runId'],
            'method': 'post',
            'name': 'reportFailed',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-status-response.json#',
            'route': '/task/<taskId>/runs/<runId>/failed',
            'stability': 'stable'},
        "rerunTask": {           'args': ['taskId'],
            'method': 'post',
            'name': 'rerunTask',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-status-response.json#',
            'route': '/task/<taskId>/rerun',
            'stability': 'deprecated'},
        "scheduleTask": {           'args': ['taskId'],
            'method': 'post',
            'name': 'scheduleTask',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-status-response.json#',
            'route': '/task/<taskId>/schedule',
            'stability': 'stable'},
        "status": {           'args': ['taskId'],
            'method': 'get',
            'name': 'status',
            'output': 'http://schemas.taskcluster.net/queue/v1/task-status-response.json#',
            'route': '/task/<taskId>/status',
            'stability': 'stable'},
        "task": {           'args': ['taskId'],
            'method': 'get',
            'name': 'task',
            'output': 'http://schemas.taskcluster.net/queue/v1/task.json#',
            'route': '/task/<taskId>',
            'stability': 'stable'},
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'Queue']
