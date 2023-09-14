import shutil
import sqlite3
import tempfile
from datetime import datetime, timezone

from hansken_extraction_plugin.api.extraction_plugin import ExtractionPlugin
from hansken_extraction_plugin.api.plugin_info import Author, MaturityLevel, PluginId, PluginInfo
from hansken_extraction_plugin.runtime.extraction_plugin_runner import run_with_hanskenpy
from logbook import Logger

log = Logger(__name__)

plugin_info = PluginInfo(
    id=PluginId(domain='hansken.org', category='extract', name='ios/battery-level'),
    version='1.0.0',
    description='Adds IOS battery level changes from knowledgeC.db as events',
    author=Author('Remco', 'remco@holmes.nl', 'NFI'),
    maturity=MaturityLevel.PROOF_OF_CONCEPT,
    webpage_url='https://hansken.org',
    license='Apache License 2.0',
    matcher='file.name=knowledgeC.db AND $data.fileType=\'SQLite 3\'',
)


def get_battery_events(database_file):
    # we'll read battery events from knowledgeC.db
    # there is much more to read than battery events, but we'll leave that as a future exercise for you, the reader
    # See also:
    # - https://www.doubleblak.com/m/blogPosts.php?id=2
    # - http://www.mac4n6.com/blog/2018/8/5/knowledge-is-power-using-the-knowledgecdb-database-on-macos-and-ios-to-determine-precise-user-and-application-usage

    with sqlite3.connect(database_file) as conn:
        conn.row_factory = sqlite3.Row
        query = """
           SELECT
               ZOBJECT.ZUUID AS "id",
               ZOBJECT.ZVALUEDOUBLE AS "text",
               ZOBJECT.ZSTREAMNAME AS "source",
               ZOBJECT.ZCREATIONDATE+978307200 AS "generatedOn",
               ZOBJECT.ZSTARTDATE+978307200 AS "startedOn",
               ZOBJECT.ZENDDATE+978307200 AS "endedOn",
               ZOBJECT.ZSECONDSFROMGMT/3600 AS "gmtoffset", 
               ZOBJECT.Z_PK AS "index"
           FROM ZOBJECT
           WHERE
               ZSTREAMNAME LIKE "/device/BatteryPercentage"
        """

        cursor = conn.cursor()
        cursor.execute(query)
        for record in cursor.fetchall():
            yield {
                'event.index': record['index'],
                'event.id': str(record['id']),
                'event.text': str(record['text']),
                'event.source': record['source'],
                'event.misc.gmtoffset': str(record['gmtoffset']),
                'event.generatedOn': datetime.fromtimestamp(int(record['generatedOn']), tz=timezone.utc),
                'event.startedOn': datetime.fromtimestamp(int(record['startedOn']), tz=timezone.utc),
                'event.endedOn': datetime.fromtimestamp(int(record['endedOn']), tz=timezone.utc),
            }


class Plugin(ExtractionPlugin):
    def plugin_info(self):
        return plugin_info

    def process(self, trace, data_context):
        log.info(f"processing trace {trace.get('name')}")

        # mark the current trace as an eventLog
        trace.update('eventLog.misc.type', 'ios-battery-level')

        # copy sqlite database to a temp_file, so it can be opened with sqlite3.connect(...)
        with tempfile.NamedTemporaryFile() as temp_file:
            shutil.copyfileobj(trace.open(), temp_file)

            # get all records from the database (lazy)
            records = get_battery_events(temp_file.name)

            # for each record create a child trace
            for event in records:
                trace.child_builder(f'battery-event-{event["event.index"]}') \
                    .update(event) \
                    .build()


if __name__ == '__main__':
    # optional main method to run your plugin with Hansken.py
    # see detail at:
    #  https://netherlandsforensicinstitute.github.io/hansken-extraction-plugin-sdk-documentation/latest/dev/python/hanskenpy.html
    run_with_hanskenpy(Plugin)
