import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 1180
    height: 760
    minimumWidth: 860
    minimumHeight: 560
    visible: true
    title: "Apex Infinite Visual"
    color: bgColor

    property var safeBridge: bridge ? bridge : fallbackBridge
    property color bgColor: safeBridge.backgroundColor
    property color panelColor: safeBridge.panelColor
    property color panelAltColor: safeBridge.panelAltColor
    property color cellColor: safeBridge.cellColor
    property color borderColor: safeBridge.borderColor
    property color lineColor: safeBridge.accentColor
    property color textColor: safeBridge.textColor
    property color mutedColor: safeBridge.mutedColor
    property color warningColor: safeBridge.warningColor
    property color errorColor: safeBridge.errorColor
    property real typeScale: safeBridge.fontScale
    property string uiFont: safeBridge.fontFamily

    QtObject {
        id: fallbackBridge

        property string themeName: "crt-green"
        property string effectiveThemeName: "crt-green"
        property string themeLabel: "Green CRT"
        property var themeNames: ["crt-green", "crt-amber", "ibm-dos", "plain"]
        property var fontFamilies: ["monospace"]
        property string fontFamily: "monospace"
        property real fontScale: 1.0
        property int effectIntensity: 0
        property real effectOpacity: 0.0
        property bool plainFallback: false
        property bool glowEnabled: false
        property bool reducedEffects: true
        property bool scanlinesEnabled: false
        property bool flickerEnabled: false
        property bool curvatureEnabled: false
        property bool hasError: false
        property bool running: false
        property bool dryRun: true
        property int maxIterations: 1
        property string statusText: "Offline"
        property string stageText: "Waiting"
        property string iterationText: "Not started"
        property string projectPath: ""
        property string startCommand: "implement"
        property string providerName: "Provider pending"
        property string modelName: "Model pending"
        property string managerOutput: "No decision yet"
        property string errorText: ""
        property var logLines: []
        property color backgroundColor: "#101419"
        property color panelColor: "#182029"
        property color panelAltColor: "#1e2732"
        property color cellColor: "#151b22"
        property color borderColor: "#303943"
        property color accentColor: "#e6edf3"
        property color textColor: "#e6edf3"
        property color mutedColor: "#8b949e"
        property color warningColor: "#d8b45f"
        property color errorColor: "#ff6f6f"

        function startRun() {}
        function stopRun() {}
        function setProjectPath(_value) {}
        function setStartCommand(_value) {}
        function setMaxIterations(_value) {}
        function setDryRun(_value) {}
        function setTheme(_value) {}
        function setEffectIntensity(_value) {}
        function setFontFamily(_value) {}
        function setFontScale(_value) {}
        function setReducedEffects(_value) {}
        function setPlainFallback(_value) {}
        function setEffectEnabled(_name, _value) {}
    }

    FontLoader {
        id: monoFont
        source: ""
    }

    Rectangle {
        anchors.fill: parent
        color: bgColor
    }

    Rectangle {
        anchors.fill: parent
        color: lineColor
        opacity: safeBridge.glowEnabled ? 0.02 + (safeBridge.effectOpacity * 0.05) : 0
    }

    Rectangle {
        anchors.fill: parent
        visible: safeBridge.scanlinesEnabled
        color: "transparent"

        Repeater {
            model: Math.ceil(root.height / 5)

            Rectangle {
                x: 0
                y: index * 5
                width: root.width
                height: 1
                color: "#000000"
                opacity: 0.08 + (safeBridge.effectOpacity * 0.18)
            }
        }
    }

    Rectangle {
        anchors.fill: parent
        visible: safeBridge.flickerEnabled
        color: "#ffffff"
        opacity: 0.0

        SequentialAnimation on opacity {
            running: safeBridge.flickerEnabled
            loops: Animation.Infinite
            NumberAnimation { to: 0.015 + (safeBridge.effectOpacity * 0.04); duration: 90; easing.type: Easing.OutQuad }
            NumberAnimation { to: 0.0; duration: 420; easing.type: Easing.InOutQuad }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 18
        spacing: 12

        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 104
            radius: safeBridge.curvatureEnabled && !safeBridge.reducedEffects ? 8 : 2
            color: panelColor
            border.color: lineColor
            border.width: 1

            GridLayout {
                anchors.fill: parent
                anchors.margins: 16
                columns: 4
                columnSpacing: 18
                rowSpacing: 8

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 3

                    Label {
                        text: "Apex Infinite Visual"
                        color: textColor
                        font.family: uiFont
                        font.pixelSize: Math.round(26 * typeScale)
                        font.bold: true
                        elide: Text.ElideRight
                        Layout.fillWidth: true
                    }

                    Label {
                        text: safeBridge.projectPath
                        color: mutedColor
                        font.family: uiFont
                        font.pixelSize: Math.round(13 * typeScale)
                        elide: Text.ElideMiddle
                        Layout.fillWidth: true
                    }
                }

                StatusCell {
                    labelText: "Status"
                    valueText: safeBridge.statusText
                    accent: safeBridge.hasError ? errorColor : lineColor
                    Layout.fillWidth: true
                }

                StatusCell {
                    labelText: "Stage"
                    valueText: safeBridge.stageText
                    accent: warningColor
                    Layout.fillWidth: true
                }

                StatusCell {
                    labelText: "Iteration"
                    valueText: safeBridge.iterationText
                    accent: lineColor
                    Layout.fillWidth: true
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 12

            Rectangle {
                Layout.preferredWidth: 330
                Layout.fillHeight: true
                radius: safeBridge.curvatureEnabled && !safeBridge.reducedEffects ? 8 : 2
                color: panelColor
                border.color: borderColor
                border.width: 1

                Flickable {
                    anchors.fill: parent
                    anchors.margins: 14
                    contentWidth: width
                    contentHeight: controlStack.implicitHeight
                    clip: true

                    ColumnLayout {
                        id: controlStack
                        width: parent.width
                        spacing: 14

                        Label {
                            text: "Run"
                            color: textColor
                            font.family: uiFont
                            font.pixelSize: Math.round(17 * typeScale)
                            font.bold: true
                        }

                        Label {
                            text: "Project"
                            color: mutedColor
                            font.family: uiFont
                            font.pixelSize: Math.round(12 * typeScale)
                        }

                        TextField {
                            text: safeBridge.projectPath
                            enabled: !safeBridge.running
                            selectByMouse: true
                            color: textColor
                            placeholderText: "Project path"
                            Layout.fillWidth: true
                            Accessible.name: "Project path"
                            onEditingFinished: safeBridge.setProjectPath(text)
                            Keys.onReturnPressed: safeBridge.setProjectPath(text)
                        }

                        Label {
                            text: "Start"
                            color: mutedColor
                            font.family: uiFont
                            font.pixelSize: Math.round(12 * typeScale)
                        }

                        TextField {
                            text: safeBridge.startCommand
                            enabled: !safeBridge.running
                            selectByMouse: true
                            color: textColor
                            placeholderText: "Start command"
                            Layout.fillWidth: true
                            Accessible.name: "Start command"
                            onEditingFinished: safeBridge.setStartCommand(text)
                            Keys.onReturnPressed: safeBridge.setStartCommand(text)
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10

                            SpinBox {
                                id: maxIterations
                                from: 1
                                to: 50
                                value: safeBridge.maxIterations
                                enabled: !safeBridge.running
                                Accessible.name: "Max iterations"
                                onValueModified: safeBridge.setMaxIterations(value)
                            }

                            CheckBox {
                                text: "Dry run"
                                checked: safeBridge.dryRun
                                enabled: !safeBridge.running
                                Accessible.name: "Dry run"
                                onToggled: safeBridge.setDryRun(checked)
                            }
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10

                            Button {
                                text: safeBridge.running ? "Running" : "Start"
                                enabled: !safeBridge.running
                                Layout.fillWidth: true
                                Accessible.name: "Start run"
                                onClicked: safeBridge.startRun()
                            }

                            Button {
                                text: "Stop"
                                enabled: safeBridge.running
                                Layout.fillWidth: true
                                Accessible.name: "Stop run"
                                onClicked: safeBridge.stopRun()
                            }
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 1
                            color: borderColor
                        }

                        Label {
                            text: "Session"
                            color: textColor
                            font.family: uiFont
                            font.pixelSize: Math.round(17 * typeScale)
                            font.bold: true
                        }

                        StatusCell {
                            labelText: "Provider"
                            valueText: safeBridge.providerName
                            accent: lineColor
                            Layout.fillWidth: true
                        }

                        StatusCell {
                            labelText: "Model"
                            valueText: safeBridge.modelName
                            accent: warningColor
                            Layout.fillWidth: true
                        }

                        StatusCell {
                            labelText: "Decision"
                            valueText: safeBridge.managerOutput
                            accent: lineColor
                            Layout.fillWidth: true
                        }

                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 1
                            color: borderColor
                        }

                        Label {
                            text: "Visual"
                            color: textColor
                            font.family: uiFont
                            font.pixelSize: Math.round(17 * typeScale)
                            font.bold: true
                        }

                        ComboBox {
                            model: safeBridge.themeNames
                            currentIndex: model.indexOf(safeBridge.themeName)
                            Layout.fillWidth: true
                            Accessible.name: "Theme"
                            onActivated: safeBridge.setTheme(currentText)
                        }

                        Label {
                            text: "Intensity " + safeBridge.effectIntensity + "%"
                            color: mutedColor
                            font.family: uiFont
                            font.pixelSize: Math.round(12 * typeScale)
                            Layout.fillWidth: true
                        }

                        Slider {
                            from: 0
                            to: 100
                            stepSize: 5
                            value: safeBridge.effectIntensity
                            enabled: !safeBridge.plainFallback
                            Layout.fillWidth: true
                            Accessible.name: "Effect intensity"
                            onMoved: safeBridge.setEffectIntensity(Math.round(value))
                        }

                        Label {
                            text: "Font"
                            color: mutedColor
                            font.family: uiFont
                            font.pixelSize: Math.round(12 * typeScale)
                            Layout.fillWidth: true
                        }

                        ComboBox {
                            model: safeBridge.fontFamilies
                            currentIndex: model.indexOf(safeBridge.fontFamily)
                            Layout.fillWidth: true
                            Accessible.name: "Font family"
                            onActivated: safeBridge.setFontFamily(currentText)
                        }

                        Label {
                            text: "Scale " + Math.round(safeBridge.fontScale * 100) + "%"
                            color: mutedColor
                            font.family: uiFont
                            font.pixelSize: Math.round(12 * typeScale)
                            Layout.fillWidth: true
                        }

                        Slider {
                            from: 0.8
                            to: 1.4
                            stepSize: 0.05
                            value: safeBridge.fontScale
                            Layout.fillWidth: true
                            Accessible.name: "Font scale"
                            onMoved: safeBridge.setFontScale(value)
                        }

                        CheckBox {
                            text: "Reduced effects"
                            checked: safeBridge.reducedEffects
                            Accessible.name: "Reduced effects"
                            onToggled: safeBridge.setReducedEffects(checked)
                        }

                        CheckBox {
                            text: "Plain fallback"
                            checked: safeBridge.plainFallback
                            Accessible.name: "Plain fallback"
                            onToggled: safeBridge.setPlainFallback(checked)
                        }

                        GridLayout {
                            Layout.fillWidth: true
                            columns: 2
                            columnSpacing: 8

                            CheckBox {
                                text: "Glow"
                                checked: safeBridge.glowEnabled
                                enabled: !safeBridge.reducedEffects && !safeBridge.plainFallback
                                Accessible.name: "Glow"
                                onToggled: safeBridge.setEffectEnabled("glow", checked)
                            }

                            CheckBox {
                                text: "Scanlines"
                                checked: safeBridge.scanlinesEnabled
                                enabled: !safeBridge.reducedEffects && !safeBridge.plainFallback
                                Accessible.name: "Scanlines"
                                onToggled: safeBridge.setEffectEnabled("scanlines", checked)
                            }

                            CheckBox {
                                text: "Flicker"
                                checked: safeBridge.flickerEnabled
                                enabled: !safeBridge.reducedEffects && !safeBridge.plainFallback
                                Accessible.name: "Flicker"
                                onToggled: safeBridge.setEffectEnabled("flicker", checked)
                            }

                            CheckBox {
                                text: "Curvature"
                                checked: safeBridge.curvatureEnabled
                                enabled: !safeBridge.reducedEffects && !safeBridge.plainFallback
                                Accessible.name: "Curvature"
                                onToggled: safeBridge.setEffectEnabled("curvature", checked)
                            }
                        }
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: safeBridge.curvatureEnabled && !safeBridge.reducedEffects ? 8 : 2
                color: panelAltColor
                border.color: safeBridge.hasError ? errorColor : lineColor
                border.width: 1

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 10

                    RowLayout {
                        Layout.fillWidth: true

                        Label {
                            text: "Event Log"
                            color: textColor
                            font.family: uiFont
                            font.pixelSize: Math.round(20 * typeScale)
                            font.bold: true
                            Layout.fillWidth: true
                        }

                        Label {
                            text: safeBridge.hasError ? safeBridge.errorText : safeBridge.statusText
                            color: safeBridge.hasError ? errorColor : mutedColor
                            font.family: uiFont
                            font.pixelSize: Math.round(13 * typeScale)
                            elide: Text.ElideRight
                            horizontalAlignment: Text.AlignRight
                            Layout.preferredWidth: 320
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 1
                        color: borderColor
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: safeBridge.hasError ? 74 : 0
                        visible: safeBridge.hasError
                        radius: safeBridge.curvatureEnabled ? 6 : 2
                        color: "#1f1517"
                        border.color: errorColor
                        border.width: 1

                        ColumnLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 4

                            Label {
                                text: safeBridge.statusText
                                color: errorColor
                                font.family: uiFont
                                font.pixelSize: Math.round(15 * typeScale)
                                font.bold: true
                                elide: Text.ElideRight
                                Layout.fillWidth: true
                            }

                            Label {
                                text: safeBridge.errorText
                                color: textColor
                                font.family: uiFont
                                font.pixelSize: Math.round(12 * typeScale)
                                wrapMode: Text.Wrap
                                maximumLineCount: 2
                                elide: Text.ElideRight
                                Layout.fillWidth: true
                            }
                        }
                    }

                    ListView {
                        id: eventLog
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        model: safeBridge.logLines
                        clip: true
                        spacing: 6
                        boundsBehavior: Flickable.StopAtBounds
                        Accessible.name: "Event log"

                        Label {
                            visible: safeBridge.logLines.length === 0
                            anchors.centerIn: parent
                            text: safeBridge.running ? "Waiting for events" : "Offline"
                            color: mutedColor
                            font.family: uiFont
                            font.pixelSize: Math.round(15 * typeScale)
                        }

                        delegate: Text {
                            required property string modelData
                            width: eventLog.width
                            text: modelData
                            color: modelData.indexOf("[ERROR]") >= 0 ? errorColor : textColor
                            font.family: uiFont
                            font.pixelSize: Math.round(14 * typeScale)
                            wrapMode: Text.Wrap
                        }

                        ScrollBar.vertical: ScrollBar {
                            policy: ScrollBar.AsNeeded
                        }
                    }
                }
            }
        }
    }

    component StatusCell: Rectangle {
        property string labelText: ""
        property string valueText: ""
        property color accent: lineColor

        implicitHeight: 58
        radius: 4
        color: cellColor
        border.color: borderColor
        border.width: 1

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 9
            spacing: 2

            Label {
                text: labelText
                color: mutedColor
                font.family: uiFont
                font.pixelSize: Math.round(11 * typeScale)
                elide: Text.ElideRight
                Layout.fillWidth: true
            }

            Label {
                text: valueText
                color: accent
                font.family: uiFont
                font.pixelSize: Math.round(15 * typeScale)
                font.bold: true
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
        }
    }
}
