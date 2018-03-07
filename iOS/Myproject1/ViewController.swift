//
//  ViewController.swift
//  Myproject1
//
//  Created by 藤田拓也 on 2018/03/07.
//  Copyright © 2018年 藤田拓也. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBAction func onButtonTap(_ sender: Any) {
        myTextfield.text = "タップされました！"
    }
    @IBOutlet weak var myTextfield: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

