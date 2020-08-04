import jaydebeapi
from jaydebeapi import *

#-----------------------------------------------------------------------------------------------------------------------
# Mapping from java.sql.Types attribute name to attribute value
_jdbc_name_to_const = None

# Mapping from java.sql.Types attribute constant value to it's attribute name
_jdbc_const_to_name = None

_jdbc_connect = None

_java_array_byte = None

_handle_sql_exception = None

def _jdbc_connect_jpype(jclassname, url, driver_args, jars, libs):
    import jpype
    if not jpype.isJVMStarted():
        args = []
        class_path = []
        if jars:
            class_path.extend(jars)
        class_path.extend(jaydebeapi._get_classpath())
        if class_path:
            args.append('-Djava.class.path=%s' %
                        os.path.pathsep.join(class_path))
        if libs:
            # path to shared libraries
            libs_path = os.path.pathsep.join(libs)
            args.append('-Djava.library.path=%s' % libs_path)
        # jvm_path = ('/usr/lib/jvm/java-6-openjdk'
        #             '/jre/lib/i386/client/libjvm.so')
        jvm_path = jpype.getDefaultJVMPath()
        jpype.startJVM(jvm_path, *args)
    if not jpype.isThreadAttachedToJVM():
        jpype.attachThreadToJVM()
    if jaydebeapi._jdbc_name_to_const is None:
        types = jpype.java.sql.Types
        types_map = {}
        if hasattr(types, '__javaclass__'):
            for i in types.__javaclass__.getClassFields():
                types_map[i.getName()] = i.getStaticAttribute()
        else:
            for k,v in types.__dict__.items():
                if "java field" in str(v):
                    types_map[k] = getattr(types, k)

        jaydebeapi._init_types(types_map)
    global _java_array_byte
    if _java_array_byte is None:
        def _java_array_byte(data):
            return jpype.JArray(jpype.JByte, 1)(data)
    # register driver for DriverManager
    jpype.JClass(jclassname)
    if isinstance(driver_args, dict):
        Properties = jpype.java.util.Properties
        info = Properties()
        for k, v in driver_args.items():
            info.setProperty(k, v)
        dargs = [info]
    else:
        dargs = driver_args
    return jpype.java.sql.DriverManager.getConnection(url, *dargs)

def _prepare_jpype():
    global _jdbc_connect
    _jdbc_connect = _jdbc_connect_jpype
    global _handle_sql_exception
    _handle_sql_exception = jaydebeapi._handle_sql_exception_jpype


if sys.platform.lower().startswith('java'):
    jaydebeapi._prepare_jython()
else:
    _prepare_jpype()
#-----------------------------------------------------------------------------------------------------------------------

def connect(jclassname, url, driver_args=None, jars=None, libs=None):
    if isinstance(driver_args, string_type):
        driver_args = [ driver_args ]
    if not driver_args:
       driver_args = []
    if jars:
        if isinstance(jars, string_type):
            jars = [ jars ]
    else:
        jars = []
    if libs:
        if isinstance(libs, string_type):
            libs = [ libs ]
    else:
        libs = []
    jconn = _jdbc_connect(jclassname, url, driver_args, jars, libs)
    return Connection(jconn, jaydebeapi._converters)

class Connection(jaydebeapi.Connection):
    def __init__(self, jconn, converters):
        # jaydebeapi.Connection.__init__(jconn, converters)
        super(Connection, self).__init__(jconn, converters)

    def cursor(self):
        return DictCursor(self, self._converters)

class DictCursor(jaydebeapi.Cursor):
    """A cursor which returns results as a dictionary"""
    def __init__(self, jconn, converters):
        # jaydebeapi.Cursor.__init__(jconn, converters)
        super(DictCursor, self).__init__(jconn, converters)

    def fetchone(self):
        if not self._rs:
            raise Error()
        if not self._rs.next():
            return None
        row = {}
        for col in range(1, self._meta.getColumnCount() + 1):
            sqltype = self._meta.getColumnType(col)
            colname = self._meta.getColumnName(col)
            converter = self._converters.get(sqltype, jaydebeapi._unknownSqlTypeConverter)
            v = converter(self._rs, col)
            row[colname]=v
        return row


