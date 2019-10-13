"""

"""
from yoyo import step


steps = [
    step('''
         CREATE TABLE "apps" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            "app_id" VARCHAR NOT NULL UNIQUE,
            "archived" BOOLEAN NOT NULL DEFAULT 0,
            "updated_at" VARCHAR NOT NULL,
            "pending_invitations" INT NOT NULL DEFAULT 0,
            "runtime" VARCHAR NULL,
            "base" VARCHAR NULL,
            "status_message" VARCHAR NULL
            )''',
         'DROP TABLE "apps"',
         ignore_errors='apply')
]
