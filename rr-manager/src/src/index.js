import AppWindow from './appWindow';
import AdvancedSearchField from './components/advancedSearchField';
import statusBox from './components/statusBox';
import statusBoxTmpl from './components/statusBoxTmpl';
import DebugGeneralTab from './panels/debug/generalTab';
import HealthPanel from './panels/healthPanel';
import SettingsGeneralTab from './panels/settings/generalTab';
import RRConfigTab from './panels/settings/rrConfigTab';
import RrManagerConfigTab from './panels/settings/rrManagerConfigTab';
import SynoInfoTab from './panels/settings/synoInfoTab';
import StatusBoxsPanel from './panels/statusBoxsPanel';
//tab addons
import Addons from './tabs/addons';
//tab debug
import Debug from './tabs/debug';
//tab main
import Main from './tabs/main';
//tab settings(configuration)
import Settings from './tabs/setting';
//tab ssh
import Ssh from './tabs/ssh';

// Namespace definition
Ext.ns('SYNOCOMMUNITY.RRManager');
// Application definition
Ext.define('SYNOCOMMUNITY.RRManager.AppInstance', {
    extend: 'SYNO.SDS.AppInstance',
    appWindowName: 'SYNOCOMMUNITY.RRManager.AppWindow',
    constructor: function () {
        this.callParent(arguments);
    }
});

SYNOCOMMUNITY.RRManager.SetEmptyIcon = (e, t) => {
    let i = e.el.child('.contentwrapper');
    if (i) {
        for (; i.child('.contentwrapper');)
            {i = i.child('.contentwrapper');}
        t && !i.hasClass('san-is-empty') ? i.addClass('san-is-empty') : !t && i.hasClass('san-is-empty') && i.removeClass('san-is-empty');
    }
};