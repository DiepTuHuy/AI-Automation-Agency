// JS code chạy trong Code Node của n8n
for (const item of $input.all()) {
  let phone = item.json.phone_number;
  if (phone) {
    // Loại bỏ ký tự đặc biệt
    phone = phone.replace(/[\s-.()]/g, '');
    // Chuyển 0 đầu thành +84
    if (phone.startsWith('0')) {
      phone = '+84' + phone.substring(1);
    }
    item.json.phone_normalized = phone;
  } else {
    item.json.phone_normalized = 'N/A';
  }
}
return $input.all();