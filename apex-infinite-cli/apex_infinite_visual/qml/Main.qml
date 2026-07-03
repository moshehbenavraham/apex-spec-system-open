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
    property color bgColor: safeBridge.themeName === "plain" ? "#101419" : "#07100d"
    property color panelColor: safeBridge.themeName === "plain" ? "#182029" : "#0b1b17"
    property color panelAltColor: safeBridge.themeName === "ibm-dos" ? "#07152a" : "#10231d"
    property color lineColor: safeBridge.themeName === "crt-amber" ? "#f0a53a" : safeBridge.themeName === "ibm-dos" ? "#62a8ff" : "#6ee7a8"
    property color textColor: safeBridge.themeName === "plain" ? "#e6edf3" : "#d8ffe7"
    property color mutedColor: safeBridge.themeName === "plain" ? "#8b949e" : "#8dbca2"
    property color warningColor: "#f2c166"
    property color errorColor: "#ff6f6f"

    QtObject {
        id: fallbackBridge

        property string themeName: "crt-green"
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

        function startRun() {}
        function stopRun() {}
        function setProjectPath(_value) {}
        function setStartCommand(_value) {}
        function setMaxIterations(_value) {}
        function setDryRun(_value) {}
        function setTheme(_value) {}
        function setReducedEffects(_value) {}
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
        opacity: safeBridge.glowEnabled && !safeBridge.reducedEffects ? 0.035 : 0
    }

    Rectangle {
        anchors.fill: parent
        visible: safeBridge.scanlinesEnabled && !safeBridge.reducedEffects
        color: "transparent"

        Repeater {
            model: Math.ceil(root.height / 5)

            Rectangle {
                x: 0
                y: index * 5
                width: root.width
                height: 1
                color: "#000000"
                opacity: 0.18
            }
        }
    }

    Rectangle {
        anchors.fill: parent
        visible: safeBridge.flickerEnabled && !safeBridge.reducedEffects
        color: "#ffffff"
        opacity: 0.0

        SequentialAnimation on opacity {
            running: safeBridge.flickerEnabled && !safeBridge.reducedEffects
            loops: Animation.Infinite
            NumberAnimation { to: 0.035; duration: 90; easing.type: Easing.OutQuad }
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
                        font.pixelSize: 26
                        font.bold: true
                        elide: Text.ElideRight
                        Layout.fillWidth: true
                    }

                    Label {
                        text: safeBridge.projectPath
                        color: mutedColor
                        font.pixelSize: 13
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
                border.color: "#253b35"
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
                            font.pixelSize: 17
                            font.bold: true
                        }

                        Label {
                            text: "Project"
                            color: mutedColor
                            font.pixelSize: 12
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
                        }

                        Label {
                            text: "Start"
                            color: mutedColor
                            font.pixelSize: 12
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
                            color: "#263c34"
                        }

                        Label {
                            text: "Session"
                            color: textColor
                            font.pixelSize: 17
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
                            color: "#263c34"
                        }

                        Label {
                            text: "Visual"
                            color: textColor
                            font.pixelSize: 17
                            font.bold: true
                        }

                        ComboBox {
                            model: ["crt-green", "crt-amber", "ibm-dos", "plain"]
                            currentIndex: model.indexOf(safeBridge.themeName)
                            Layout.fillWidth: true
                            Accessible.name: "Theme"
                            onActivated: safeBridge.setTheme(currentText)
                        }

                        CheckBox {
                            text: "Reduced effects"
                            checked: safeBridge.reducedEffects
                            Accessible.name: "Reduced effects"
                            onToggled: safeBridge.setReducedEffects(checked)
                        }

                        GridLayout {
                            Layout.fillWidth: true
                            columns: 2
                            columnSpacing: 8

                            CheckBox {
                                text: "Glow"
                                checked: safeBridge.glowEnabled
                                enabled: !safeBridge.reducedEffects
                                Accessible.name: "Glow"
                                onToggled: safeBridge.setEffectEnabled("glow", checked)
                            }

                            CheckBox {
                                text: "Scanlines"
                                checked: safeBridge.scanlinesEnabled
                                enabled: !safeBridge.reducedEffects
                                Accessible.name: "Scanlines"
                                onToggled: safeBridge.setEffectEnabled("scanlines", checked)
                            }

                            CheckBox {
                                text: "Flicker"
                                checked: safeBridge.flickerEnabled
                                enabled: !safeBridge.reducedEffects
                                Accessible.name: "Flicker"
                                onToggled: safeBridge.setEffectEnabled("flicker", checked)
                            }

                            CheckBox {
                                text: "Curvature"
                                checked: safeBridge.curvatureEnabled
                                enabled: !safeBridge.reducedEffects
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
                            font.pixelSize: 20
                            font.bold: true
                            Layout.fillWidth: true
                        }

                        Label {
                            text: safeBridge.hasError ? safeBridge.errorText : safeBridge.statusText
                            color: safeBridge.hasError ? errorColor : mutedColor
                            font.pixelSize: 13
                            elide: Text.ElideRight
                            horizontalAlignment: Text.AlignRight
                            Layout.preferredWidth: 320
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 1
                        color: "#2f4b40"
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

                        delegate: Text {
                            required property string modelData
                            width: eventLog.width
                            text: modelData
                            color: modelData.indexOf("[ERROR]") >= 0 ? errorColor : textColor
                            font.family: "monospace"
                            font.pixelSize: 14
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
        color: "#111c19"
        border.color: "#263c34"
        border.width: 1

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 9
            spacing: 2

            Label {
                text: labelText
                color: mutedColor
                font.pixelSize: 11
                elide: Text.ElideRight
                Layout.fillWidth: true
            }

            Label {
                text: valueText
                color: accent
                font.pixelSize: 15
                font.bold: true
                elide: Text.ElideRight
                Layout.fillWidth: true
            }
        }
    }
}
