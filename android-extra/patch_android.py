import re, sys, pathlib
root = pathlib.Path(sys.argv[1])
man = root / 'app/src/main/AndroidManifest.xml'
s = man.read_text()
perms = ['READ_STEPS', 'READ_EXERCISE', 'READ_ACTIVE_CALORIES_BURNED', 'READ_TOTAL_CALORIES_BURNED', 'READ_DISTANCE']
bloco = '\n'.join(f'    <uses-permission android:name="android.permission.health.{p}" />' for p in perms)
bloco += '\n    <queries>\n        <package android:name="com.google.android.apps.healthdata" />\n    </queries>\n'
s = s.replace('</manifest>', bloco + '</manifest>')
atividade = '''
        <activity
            android:name="com.fit_up.health.capacitor.PermissionsRationaleActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="androidx.health.ACTION_SHOW_PERMISSIONS_RATIONALE" />
            </intent-filter>
        </activity>
        <activity-alias
            android:name="ViewPermissionUsageActivity"
            android:exported="true"
            android:targetActivity="com.fit_up.health.capacitor.PermissionsRationaleActivity"
            android:permission="android.permission.START_VIEW_PERMISSION_USAGE">
            <intent-filter>
                <action android:name="android.intent.action.VIEW_PERMISSION_USAGE" />
                <category android:name="android.intent.category.HEALTH_PERMISSIONS" />
            </intent-filter>
        </activity-alias>
'''
s = s.replace('</application>', atividade + '    </application>')
man.write_text(s)
var = root / 'variables.gradle'
v = var.read_text()
v = re.sub(r'minSdkVersion\s*=\s*\d+', 'minSdkVersion = 26', v)
var.write_text(v)
print(s); print(v)
