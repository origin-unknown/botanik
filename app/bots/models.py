from .. import db

import os, subprocess

class Bot(db.Model):
    __tablename__ = 'bots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,
        unique=True,
        nullable=False,
        index=True
    )

    # The commando to start the application.
    command = db.Column(db.String,
        nullable=False
    )

    # The process id to end the respective process again.
    pid = db.Column(db.Integer,
        nullable=False,
        default=0
    )

    @property
    def is_running(self):
        return self.pid != 0

    # If a bot is to be started via account, the implementation must be adjusted.
    def launch(self):
        '''Start the application in a sub-process within the shell.'''
        if not self.is_running:
            command_line = self.command
            proc = subprocess.Popen(
                command_line,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=True,
            )
            self.pid = proc.pid
            db.session.commit()
        return self

    def kill(self):
        '''Terminate the associated subprocess based on its id.'''
        if self.is_running:
            try:
                os.kill(self.pid, 9)
            except OSError:
                pass
        self.pid = 0
        db.session.commit()
        return self
