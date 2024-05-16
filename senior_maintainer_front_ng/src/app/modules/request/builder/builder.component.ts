import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { NgbModal, NgbModalConfig } from '@ng-bootstrap/ng-bootstrap';
import { ApproveUserField } from 'src/app/model/ApproveUserField.model';
import { DatabaseField } from 'src/app/model/DatabaseField.model';
import { MaintainerFormData } from 'src/app/model/MaintainerFormData.model';
import { MaintainerService } from 'src/app/services/maintainer.service';
import { NgxSpinnerService } from 'ngx-spinner';
import Swal, { SweetAlertIcon } from 'sweetalert2';
import { ConsultModel } from 'src/app/model/Consult.model';
import { ConsultVerifyResponseModel } from 'src/app/model/ConsultVerifyResponse.model';
import { firstValueFrom } from 'rxjs';
import { RequestModel } from 'src/app/model/Request.model';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.css'],
  providers: [NgbModalConfig, NgbModal],
})
export class BuilderComponent implements OnInit {
  userInfo = this.msAuth.userInfo();
  currentTime: Date = new Date();
  activeSendRequest: boolean = false;
  requester_name = this.userInfo?.name;
  requester_email = this.userInfo?.username;
  query_validated: boolean = false;
  fields: MaintainerFormData = new MaintainerFormData();
  requestForm: FormGroup;
  requestTransactionStatus: boolean = false;
  records: number = 0;
  constructor(
    private formBuilder: FormBuilder,
    config: NgbModalConfig,
    private modalService: NgbModal,
    private maintainerService: MaintainerService,
    private spinner: NgxSpinnerService,
    private msAuth: AuthService
  ) {

    this.requestForm = formBuilder.group({
      query: new FormControl(null, [
        Validators.required,
        Validators.nullValidator,
      ]),
      database: new FormControl(null, [
        Validators.required,
        Validators.nullValidator,
      ]),
      number_of_records: new FormControl(0, [
        Validators.required,
        Validators.nullValidator,
        Validators.min(0),
      ]),
      approver_email: new FormControl(null, [
        Validators.required,
        Validators.nullValidator,
      ]),
      description: new FormControl(null, [
        Validators.required,
        Validators.nullValidator,
      ]),
    });

    this.msAuth.refreshToken()

    this.requestForm.controls['number_of_records'].disable()
  }

  ngOnInit(): void {
    setInterval(() => {
      this.currentTime = new Date();
    }, 1000);
    this.spinner.show();
    this.maintainerService.getFields().subscribe((data) => {
      let fieldsEntry = JSON.parse(Object.values(data)[1]);
      fieldsEntry['database_list'].map((database: DatabaseField) =>
        this.fields.database_list.push(database)
      );
      fieldsEntry['approve_user_list'].map((user: ApproveUserField) =>
        this.fields.approve_user_list.push(user)
      );
      this.spinner.hide();
    });
  }

  validateQuery(): void {
    let validationInfo: ConsultVerifyResponseModel =
      new ConsultVerifyResponseModel();
    Swal.fire({
      title: 'Solicitando validación de consulta',
      timerProgressBar: true,
      didOpen: () => {
        Swal.showLoading();
        let consult = new ConsultModel(
          this.requestForm.get('query')?.value,
          this.requestForm.get('database')?.value
        );
        this.maintainerService.validateQuery(consult).subscribe((response) => {
          validationInfo['msg_error'] = JSON.parse(Object.values(response)[1])[
            'msg_error'
          ];
          validationInfo['rowcount'] = JSON.parse(Object.values(response)[1])[
            'rowcount'
          ];
          Swal.close();
        });
      },
    }).then((result) => {
      if (result.isDismissed) {
        let status_message = '';
        let row_status_message = '';
        let error_status_message = '';
        let icon_type: SweetAlertIcon = 'info';
        this.records = validationInfo.rowcount;
        if (validationInfo.rowcount > 0 && validationInfo.msg_error === '') {
          status_message =
            'Se ha ejecutado la validación correctamente con el siguiente resultado:\n';
          row_status_message =
            '- La consulta afecta ' +
            String(validationInfo.rowcount.toLocaleString()) +
            ' registros.\n';
          this.activeSendRequest = true;
        } else if (
          validationInfo.msg_error === '' &&
          validationInfo.rowcount == 0
        ) {
          status_message = 'No se ha ejecutado la validación correctamente.';
          icon_type = 'error';
          this.activeSendRequest = false;
        } else if (validationInfo.msg_error !== '') {
          status_message =
            'Se ha ejecutado la validación y ha generado el siguiente mensaje: ';
          error_status_message = '- ' + String(validationInfo.msg_error) + '\n';
          this.activeSendRequest = false;
        }
        Swal.fire({
          title: status_message,
          html: row_status_message + error_status_message,
          icon: icon_type,
        });
      }
    });
  }

  sendRequest(): void {
    let msg_response: string;
    Swal.fire({
      title: 'Solicitando validación de consulta',
      timerProgressBar: true,
      didOpen: () => {
        let requestToSend = new RequestModel(
          this.requestForm.get('query')?.value,
          this.requestForm.get('database')?.value,
          this.requestForm.get('number_of_records')?.value,
          this.requester_email ?? '',
          this.requestForm.get('approver_email')?.value,
          this.requestForm.get('description')?.value,
          this.requester_name ?? ''
        );

        Swal.showLoading();
        this.maintainerService
          .sendRequest(requestToSend)
          .subscribe((response) => {
            console.log(response)
            Swal.close();
          });
      },
    });
  }

  cleanForm() {
    this.requestForm.reset()
  }

}
