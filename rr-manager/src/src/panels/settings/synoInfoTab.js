export default Ext.define('SYNOCOMMUNITY.RRManager.Setting.SynoInfoTab', {
  extend: 'SYNO.SDS.Utils.FormPanel',
  constructor: function (e) {
    this.callParent([this.fillConfig(e)]);
  },
  fillConfig: function (e) {
    this.suspendLcwPrompt = !1;
    const t = {
      title: 'Syno Info',
      items: [
        new SYNO.ux.FieldSet({
          title: 'SynoInfo Config',
          collapsible: true,
          name: 'synoinfo',
          items: [
            {
              fieldLabel: 'maxdisks', 
              name: 'maxdisks',
              allowBlank: true,
              xtype: 'syno_numberfield',
            },
            {
              fieldLabel: 'internalportcfg',
              name: 'internalportcfg',
              allowBlank: true,
              xtype: 'syno_numberfield',
            },
            {
              fieldLabel: 'esataportcfg',
              name: 'esataportcfg',
              allowBlank: true,
              xtype: 'syno_textfield',
            },
            {
              fieldLabel: 'usbportcfg',
              name: 'usbportcfg',
              allowBlank: true,
              xtype: 'syno_textfield',
            },
            {
              fieldLabel: 'max_sys_raid_disks',
              name: 'max_sys_raid_disks',
              allowBlank: true,
              xtype:'syno_numberfield',
            }
          ],
        }),
      ],
    };
    return Ext.apply(t, e), t;
  },
  initEvents: function () {
    this.mon(this, 'activate', this.onActivate, this);
  },
  onActivate: function () {},
  loadForm: function (e) {
    this.getForm().setValues(e);
  },
  promptLcwDialog: function (e, t) {
    t &&
      !this.suspendLcwPrompt &&
      this.appWin.getMsgBox().show({
        title: this.title,
        msg: 'ddd',
        buttons: {
          yes: {
            text: Ext.MessageBox.buttonText.yes,
            btnStyle: 'red',
          },
          no: {
            text: Ext.MessageBox.buttonText.no,
          },
        },
        fn: function (e) {
          'yes' !== e && this.form.findField('lcw_enabled').setValue(!1);
        },
        scope: this,
        icon: Ext.MessageBox.ERRORRED,
        minWidth: Ext.MessageBox.minWidth,
      });
  },
});
