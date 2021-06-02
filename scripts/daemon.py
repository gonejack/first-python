#!/usr/bin/env python2.7
# coding: utf-8

import glob
import os
import re
import sys
import time
import atexit
import signal
import logging
import subprocess
from logging.handlers import RotatingFileHandler


class Daemon(object):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = os.path.abspath(stdin)
        self.stdout = os.path.abspath(stdout)
        self.stderr = os.path.abspath(stderr)
        self.pidfile = os.path.abspath(pidfile)

    def daemonize(self):
        if self.fork() != 0:
            os.waitpid(0, 0)
            time.sleep(1)
            return

        if self.fork() != 0:
            sys.exit(0)

        self.detach_env()

        sys.stdout.flush()
        sys.stderr.flush()

        self.attach_stream('stdin', mode='r')
        self.attach_stream('stdout', mode='a+')
        self.attach_stream('stderr', mode='a+')

        # write pidfile
        self.create_pidfile()

        # run
        self.run()
        sys.exit(0)

    def attach_stream(self, name, mode):
        stream = open(getattr(self, name), mode)
        os.dup2(stream.fileno(), getattr(sys, name).fileno())

    @staticmethod
    def detach_env():
        os.chdir("/")
        os.setsid()
        os.umask(0)

    @staticmethod
    def fork():
        try:
            return os.fork()
        except OSError as e:
            sys.stderr.write("Fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

    def create_pidfile(self):
        atexit.register(self.remove_pid)
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write("%s\n" % pid)

    def remove_pid(self):
        os.remove(self.pidfile)

    def start(self):
        pid = self.get_pid()

        if pid:
            message = "pidfile %s exist, already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        self.daemonize()

    def get_pid(self):
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except (IOError, TypeError):
            pid = None
        return pid

    def stop(self, silent=False):
        pid = self.get_pid()

        if not pid:
            if not silent:
                message = "pidfile %s not exist.\n"
                sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                sys.stdout.write(str(err))
                sys.exit(1)

    def restart(self):
        self.stop(silent=True)
        self.start()

    def op_start(self):
        print("Starting:")
        self.start()
        self.op_status(
            running='Done[pid=%d]',
            not_running='Fail'
        )

    def op_stop(self):
        print("Stopping:")
        self.stop(True)
        self.op_status(
            running='Fail[pid=%d]',
            not_running='Done'
        )

    def op_restart(self):
        self.op_stop()
        self.op_start()

    def op_status(self, running='Running[pid=%d]', not_running='Not Running'):
        pid = self.get_pid()
        if pid:
            print(running % pid)
        else:
            print(not_running)

    def run(self):
        raise NotImplementedError

    def entry(self):
        acts = ("start", "stop", "restart", "status")

        if sys.argv[1:] and sys.argv[1] in acts:
            getattr(self, "op_" + sys.argv[1])()
        else:
            print("Usage: %s [%s]" % (__file__, str.join("|", acts)))


class Sync(Daemon):
    def __init__(self, run_log='./test2.log', pidfile='./test2.pid'):
        logging.basicConfig(
            level=logging.INFO
        )

        handler = RotatingFileHandler(run_log, maxBytes=1024 * 1024 * 5, backupCount=5)
        handler.setFormatter(logging.Formatter(
            fmt='%(asctime)-15s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
        )

        self.logger = logging.getLogger('logger')
        self.logger.addHandler(handler)

        super(Sync, self).__init__(pidfile=pidfile)

    def run(self):
        while 1:
            time.sleep(3)
            try:
                p = subprocess.Popen(['ls', '/x'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
                if p.returncode:
                    raise Exception(err)
                else:
                    return out
            except Exception as e:
                self.logger.error(e)


Sync().entry()
