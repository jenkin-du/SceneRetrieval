namespace SceneRetrieval.form
{
    partial class DrawSceneForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(DrawSceneForm));
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.selectMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.addMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.deleteMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.stopMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.clearMenu = new System.Windows.Forms.ToolStripMenuItem();
            this.drawMap = new ESRI.ArcGIS.Controls.AxMapControl();
            this.menuStrip1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.drawMap)).BeginInit();
            this.SuspendLayout();
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.selectMenu,
            this.addMenu,
            this.deleteMenu,
            this.stopMenu,
            this.clearMenu});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(408, 25);
            this.menuStrip1.TabIndex = 0;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // selectMenu
            // 
            this.selectMenu.Name = "selectMenu";
            this.selectMenu.Size = new System.Drawing.Size(44, 21);
            this.selectMenu.Text = "选择";
            this.selectMenu.Click += new System.EventHandler(this.selectMenu_Click);
            // 
            // addMenu
            // 
            this.addMenu.Name = "addMenu";
            this.addMenu.Size = new System.Drawing.Size(44, 21);
            this.addMenu.Text = "添加";
            this.addMenu.Click += new System.EventHandler(this.startMenu_Click);
            // 
            // deleteMenu
            // 
            this.deleteMenu.Name = "deleteMenu";
            this.deleteMenu.Size = new System.Drawing.Size(44, 21);
            this.deleteMenu.Text = "删除";
            this.deleteMenu.Click += new System.EventHandler(this.deleteMenu_Click);
            // 
            // stopMenu
            // 
            this.stopMenu.Name = "stopMenu";
            this.stopMenu.Size = new System.Drawing.Size(44, 21);
            this.stopMenu.Text = "保存";
            this.stopMenu.Click += new System.EventHandler(this.stopMenu_Click);
            // 
            // clearMenu
            // 
            this.clearMenu.Name = "clearMenu";
            this.clearMenu.Size = new System.Drawing.Size(44, 21);
            this.clearMenu.Text = "清屏";
            this.clearMenu.Click += new System.EventHandler(this.clearMenu_Click);
            // 
            // drawMap
            // 
            this.drawMap.Dock = System.Windows.Forms.DockStyle.Fill;
            this.drawMap.Location = new System.Drawing.Point(0, 25);
            this.drawMap.Name = "drawMap";
            this.drawMap.OcxState = ((System.Windows.Forms.AxHost.State)(resources.GetObject("drawMap.OcxState")));
            this.drawMap.Size = new System.Drawing.Size(408, 305);
            this.drawMap.TabIndex = 1;
            // 
            // DrawSceneForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(408, 330);
            this.Controls.Add(this.drawMap);
            this.Controls.Add(this.menuStrip1);
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "DrawSceneForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "绘制场景";
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.DrawSceneForm_FormClosed);
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.drawMap)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem addMenu;
        private System.Windows.Forms.ToolStripMenuItem stopMenu;
        private System.Windows.Forms.ToolStripMenuItem clearMenu;
        private ESRI.ArcGIS.Controls.AxMapControl drawMap;
        private System.Windows.Forms.ToolStripMenuItem selectMenu;
        private System.Windows.Forms.ToolStripMenuItem deleteMenu;
    }
}