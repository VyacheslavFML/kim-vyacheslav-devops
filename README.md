# DevOps Fundamentals

Personal laboratory project by Ким Вячеслав Александрович, IT2-2312.

Student ID: 37746. Course: DevOps.

## Project naming

- Directory: `~/devops/kim_vyacheslav`
- Information: `Kim_Vyacheslav_info.txt`
- System script: `scripts/Kim_Vyacheslav_system.sh`
- GitHub repository and Docker image: `kim-vyacheslav-devops`
- Application container: `kim-vyacheslav-container`
- Jenkins job: `Kim_Vyacheslav_DevOps`

## Run and verify

```bash
python3 -m unittest discover -s tests -v
docker build -t kim-vyacheslav-devops .
docker run -d --name kim-vyacheslav-container -p 127.0.0.1:8081:8080 \
  -e STUDENT_NAME=Vyacheslav -e STUDENT_SURNAME=Kim \
  -e STUDENT_GROUP=IT2-2312 -e STUDENT_ID=37746 kim-vyacheslav-devops
curl http://localhost:8081/
curl http://localhost:8081/health
docker logs kim-vyacheslav-container
docker stop kim-vyacheslav-container
docker rm kim-vyacheslav-container
docker compose up -d
docker compose ps
docker compose down
```

The web application exposes `/` (student text), `/student` (JSON), and `/health`.
Python's standard library is sufficient; no third-party application dependencies are needed.
The image runs as the unprivileged `student` user. Host ports bind to loopback.
Environment variables override the sample student defaults without rebuilding the image.
Never place passwords or API tokens in the Dockerfile, Git repository, or report.

## Linux commands and permissions

`pwd` prints the current directory; `ls` lists entries; `cd` changes directory;
`mkdir` creates directories; `touch` creates an empty file or updates its timestamp;
`cp` copies; `mv` moves or renames; `rm` removes; `cat` prints file content;
`head` and `tail` print its beginning and end. `find` locates files, and `grep`
filters lines. `grep -c ERROR logs/application.log` counts matching lines.

`chmod 600 private.txt` grants only the owner read/write access.
`chmod 644 public.txt` also lets group and others read the file.
The permission bits `r`, `w`, `x` mean read, write, and execute; for directories,
execute permits traversal. The three groups describe owner, group members, and
others. `chmod 755` grants owner rwx and everyone else r-x. Git preserves the
executable bit, but does not preserve all Unix permission bits: repeat `chmod`
after cloning if necessary.

A process is a running program. Its PID identifies it within the process namespace.
`ps` takes a snapshot; `ps aux` lists processes with owner, PID, CPU and memory use;
`top` updates these values interactively (`top -b -n 1` takes a batch snapshot).
The system script uses `whoami`, `hostname`, `date`, `uname`, `df`, and `free`.
Run it on Linux, including a Linux container or VM, because macOS has no `free`.

## Git and GitHub

The commit history records actual incremental work. `development` added the
Jenkins pipeline and was merged into `main` with a merge commit. Branches isolate
changes so work can be reviewed before integration. `git push` sends local commits
to a remote; `git pull` fetches remote changes and integrates them locally.
`.gitignore` excludes logs, backups, `.env`, and Python caches; these files can
contain volatile output or secrets and do not belong in version control.

## Jenkins pipeline

Create a Pipeline job named `Kim_Vyacheslav_DevOps`. Select **Pipeline script from
SCM**, choose Git, and use this repository URL with branch `*/main` and script path
`Jenkinsfile`. The Jenkins agent needs Git, Python 3, Docker CLI, and access to a
Docker daemon. Required plugins include Pipeline, Git, and Timestamper; Pipeline
Stage View provides stage visualization.

1. **Checkout** obtains the GitHub commit and prints its SHA and student details.
2. **Build** compiles the Python sources to check syntax.
3. **Test** checks the defaults and all environment-variable overrides.
4. **Docker Build** builds the application image and runs tests during image build.
5. **Docker Run** starts the container, retries readiness checks, checks the actual
   HTTP response against `STUDENT_ID`, and displays logs and the running container.

A failed stage marks the build as failed and prevents subsequent normal stages.
The `post` block still reports the final result. Do not interpret a built image
alone as a successful deployment: the HTTP assertion must also pass.

## Integrated workflow

Linux provides the filesystem, permissions, processes, and runtime. Git records
changes locally. GitHub stores and shares those commits. Jenkins checks out a
specific GitHub revision, builds and tests it, packages it as a Docker image, and
starts a container from that image. The image is a reusable filesystem/configuration
template; the container is a running instance with its own runtime state. Compose
stores service settings declaratively so repeatable startup and cleanup require
only a few commands. This pipeline is started manually from Jenkins; a webhook
is optional and is not required by the assignment.
