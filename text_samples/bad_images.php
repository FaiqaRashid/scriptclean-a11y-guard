<?php
/**
 * ============================================================
 * TEST SAMPLE: bad_images.php
 * ScriptClean A11y Guard — Intentionally Inaccessible File
 *
 * PURPOSE: Demo file for IBM Bob hackathon. Contains deliberate
 * WCAG violations for ScriptClean to detect and fix.
 *
 * VIOLATIONS IN THIS FILE:
 *   [L58]  CRITICAL — product image, no alt attribute
 *   [L66]  CRITICAL — chart/data visualization image, no alt
 *   [L80]  CRITICAL — modal close button, aria-label missing
 *   [L95]  CRITICAL — search input, no label or aria-label
 *   [L112] CRITICAL — file upload input, no label
 *   [L124] WARNING  — decorative divider <img>, missing alt=""
 *   [L134] WARNING  — icon-only edit/delete buttons, no labels
 *   [L158] WARNING  — role="dialog" modal missing aria-labelledby
 *   [L172] INFO     — <table> has no <caption> or aria-label
 *   [L196] CRITICAL — password input, no associated <label>
 *   [L210] WARNING  — progress bar has no aria-valuenow/valuemin/valuemax
 * ============================================================
 */

// Simulate PHP backend logic
$page_title = "ShopDash — Product Manager";
$products = [
    ["id" => 1, "name" => "Wireless Headphones Pro", "price" => 149.99, "stock" => 43, "img" => "headphones.jpg"],
    ["id" => 2, "name" => "Mechanical Keyboard RGB", "price" => 89.99, "stock" => 12, "img" => "keyboard.jpg"],
    ["id" => 3, "name" => "4K Webcam Ultra", "price" => 199.99, "stock" => 7, "img" => "webcam.jpg"],
];
$total_revenue = 24850.75;
$orders_today = 38;
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title><?php echo htmlspecialchars($page_title); ?></title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0}body{font-family:'Segoe UI',sans-serif;background:#f4f4f4;color:#333}
    .header{background:#161616;color:#fff;padding:1rem 2rem;display:flex;justify-content:space-between;align-items:center}
    .container{max-width:1100px;margin:2rem auto;padding:0 1rem}
    .card{background:#fff;border:1px solid #e0e0e0;padding:1.5rem;margin-bottom:1.5rem}
    .btn{padding:8px 18px;border:none;cursor:pointer;font-size:13px;font-family:inherit}
    .btn-primary{background:#0f62fe;color:#fff}.btn-danger{background:#da1e28;color:#fff}
    .btn-ghost{background:transparent;border:1px solid #0f62fe;color:#0f62fe}
    table{width:100%;border-collapse:collapse;font-size:14px}
    th{text-align:left;padding:10px 12px;background:#f4f4f4;font-weight:600;border-bottom:2px solid #e0e0e0}
    td{padding:10px 12px;border-bottom:1px solid #e0e0e0;vertical-align:middle}
    input,select{padding:9px 12px;border:1px solid #ccc;font-size:14px;font-family:inherit;width:100%}
    .badge{font-size:11px;padding:2px 8px;font-weight:600}
    .badge-low{background:#fff1f1;color:#da1e28}.badge-ok{background:#defbe6;color:#198038}
    .modal-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);display:none;align-items:center;justify-content:center;z-index:1000}
    .modal-overlay.open{display:flex}
    .modal{background:#fff;padding:2rem;width:480px;max-width:90%;position:relative}
    .progress-bar-wrap{background:#e0e0e0;height:8px;border-radius:4px;overflow:hidden;margin:.5rem 0}
    .progress-fill{height:100%;background:#0f62fe;border-radius:4px}
  </style>
</head>
<body>

<header class="header">
  <div style="font-size:16px;font-weight:600;">ShopDash</div>
  <div style="display:flex;gap:1rem;align-items:center;">
    <!-- ====================================================
      VIOLATION 1 (CRITICAL — WCAG 4.1.2):
      Notification bell icon button. Icon only, no aria-label.
      BOB SHOULD FIX: aria-label="View notifications (3 unread)"
    ===================================================== -->
    <button onclick="openNotifications()" style="background:none;border:none;cursor:pointer;color:#fff;position:relative;">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 01-3.46 0"/></svg>
      <span style="position:absolute;top:-4px;right:-4px;background:#da1e28;color:#fff;font-size:10px;width:16px;height:16px;border-radius:50%;display:flex;align-items:center;justify-content:center;">3</span>
    </button>
    <img src="assets/avatar-admin.jpg" style="width:32px;height:32px;border-radius:50%;">
  </div>
</header>

<div class="container">

  <!-- Stats Row -->
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.5rem;">
    <div class="card" style="padding:1.25rem;">
      <p style="font-size:12px;color:#6f6f6f;text-transform:uppercase;letter-spacing:.4px;margin-bottom:.4rem;">Total Revenue</p>
      <p style="font-size:28px;font-weight:300;">$<?php echo number_format($total_revenue, 2); ?></p>
    </div>
    <div class="card" style="padding:1.25rem;">
      <p style="font-size:12px;color:#6f6f6f;text-transform:uppercase;letter-spacing:.4px;margin-bottom:.4rem;">Orders Today</p>
      <p style="font-size:28px;font-weight:300;"><?php echo $orders_today; ?></p>
      <!-- ====================================================
        VIOLATION 2 (CRITICAL — WCAG 1.1.1):
        Revenue trend chart rendered as <img>. Conveys actual
        business data (upward trend). No alt attribute.
        BOB SHOULD FIX: alt="Revenue trend chart showing 23% increase over the past 7 days"
      ===================================================== -->
      <img src="assets/revenue-chart-sparkline.png" style="width:100%;margin-top:.5rem;">
    </div>
    <div class="card" style="padding:1.25rem;">
      <p style="font-size:12px;color:#6f6f6f;text-transform:uppercase;letter-spacing:.4px;margin-bottom:.4rem;">Conversion Rate</p>
      <p style="font-size:28px;font-weight:300;">4.7%</p>
      <!-- ====================================================
        VIOLATION 3 (CRITICAL — WCAG 1.1.1):
        A bar chart showing conversion rate breakdown.
        This image conveys essential analytics data.
        BOB SHOULD FIX: alt="Bar chart: 4.7% average conversion rate, up from 3.9% last month"
      ===================================================== -->
      <img src="assets/conversion-chart.png" style="width:100%;margin-top:.5rem;">
    </div>
  </div>

  <!-- Search & Filter -->
  <div class="card">
    <div style="display:flex;gap:1rem;align-items:flex-end;">
      <div style="flex:1;">
        <p style="font-size:12px;font-weight:600;margin-bottom:.4rem;color:#6f6f6f;">SEARCH PRODUCTS</p>
        <!-- ====================================================
          VIOLATION 4 (CRITICAL — WCAG 4.1.2):
          Search input has no associated <label> and no aria-label.
          The placeholder disappears on focus — NOT a substitute.
          BOB SHOULD FIX:
            <label for="product-search">Search products</label>
            <input id="product-search" aria-label="Search products by name or SKU">
        ===================================================== -->
        <input type="text" id="product-search" placeholder="Search by name, SKU, or category..." onkeyup="filterProducts(this.value)">
      </div>
      <div>
        <select style="width:auto;">
          <option>All Categories</option>
          <option>Electronics</option>
          <option>Accessories</option>
        </select>
      </div>
      <!-- ====================================================
        VIOLATION 5 (CRITICAL — WCAG 4.1.2):
        Filter icon button with no accessible label.
        BOB SHOULD FIX: aria-label="Open advanced filter options"
      ===================================================== -->
      <button onclick="openFilters()" style="background:none;border:1px solid #ccc;padding:9px;cursor:pointer;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="6" x2="20" y2="6"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="11" y1="18" x2="13" y2="18"/></svg>
      </button>
    </div>
  </div>

  <!-- ========================================================
    VIOLATION 6 (WARNING — WCAG 1.1.1):
    Decorative divider image (horizontal rule graphic).
    Decorative images MUST have alt="" to be safely skipped
    by screen readers. Missing alt is still a violation.
    BOB SHOULD FIX: alt="" role="presentation"
  ========================================================= -->
  <img src="assets/section-divider.svg" style="width:100%;height:8px;display:block;margin:.5rem 0;">

  <!-- Product Table -->
  <div class="card" style="padding:0;overflow:hidden;">
    <!-- ======================================================
      VIOLATION 7 (INFO — WCAG 1.3.1):
      Data table has no <caption> and no aria-label.
      Screen readers need context about what the table contains.
      BOB SHOULD FIX: Add <caption>Product inventory list</caption>
      or aria-label="Product inventory list" on the <table>
    ======================================================= -->
    <table>
      <thead>
        <tr>
          <th>Product</th>
          <th>Price</th>
          <th>Stock</th>
          <th>Upload Image</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <?php foreach ($products as $product): ?>
        <tr>
          <td style="display:flex;align-items:center;gap:12px;">
            <!-- ============================================
              VIOLATION 8 (CRITICAL — WCAG 1.1.1):
              Product image inside a table row. No alt attribute.
              BOB SHOULD FIX: alt="<?php echo htmlspecialchars($product['name']); ?> product thumbnail"
            ============================================= -->
            <img src="assets/products/<?php echo $product['img']; ?>" style="width:48px;height:48px;object-fit:cover;border:1px solid #e0e0e0;">
            <span><?php echo htmlspecialchars($product['name']); ?></span>
          </td>
          <td>$<?php echo number_format($product['price'], 2); ?></td>
          <td>
            <span class="badge <?php echo $product['stock'] < 10 ? 'badge-low' : 'badge-ok'; ?>">
              <?php echo $product['stock']; ?> units
            </span>
          </td>
          <td>
            <!-- ============================================
              VIOLATION 9 (CRITICAL — WCAG 4.1.2):
              File input to upload a new product image.
              No <label> and no aria-label. Screen readers
              will announce "Choose File" with zero context.
              BOB SHOULD FIX:
                <label for="upload-<?php echo $product['id']; ?>">
                  Upload new image for <?php echo htmlspecialchars($product['name']); ?>
                </label>
            ============================================= -->
            <input type="file" id="upload-<?php echo $product['id']; ?>" accept="image/*" onchange="handleUpload(this, <?php echo $product['id']; ?>)">
          </td>
          <td>
            <!-- ============================================
              VIOLATION 10 (WARNING — WCAG 4.1.2):
              Edit and Delete buttons contain only SVG icons.
              No aria-label — screen readers cannot distinguish
              which product is being acted on.
              BOB SHOULD FIX:
                aria-label="Edit <?php echo htmlspecialchars($product['name']); ?>"
                aria-label="Delete <?php echo htmlspecialchars($product['name']); ?>"
            ============================================= -->
            <div style="display:flex;gap:6px;">
              <button onclick="editProduct(<?php echo $product['id']; ?>)" class="btn btn-ghost" style="padding:6px;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
              </button>
              <button onclick="deleteProduct(<?php echo $product['id']; ?>)" class="btn btn-danger" style="padding:6px;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 011-1h4a1 1 0 011 1v2"/></svg>
              </button>
            </div>
          </td>
        </tr>
        <?php endforeach; ?>
      </tbody>
    </table>
  </div>

  <!-- Upload Progress -->
  <div class="card" id="upload-progress" style="display:none;">
    <p style="font-size:13px;font-weight:600;margin-bottom:.75rem;">Uploading image...</p>
    <!-- ======================================================
      VIOLATION 11 (WARNING — WCAG 4.1.2):
      Progress bar has no ARIA attributes. Screen readers
      cannot convey upload progress to visually impaired users.
      BOB SHOULD FIX:
        role="progressbar"
        aria-valuenow="65"
        aria-valuemin="0"
        aria-valuemax="100"
        aria-label="Image upload progress"
    ======================================================= -->
    <div class="progress-bar-wrap">
      <div class="progress-fill" id="progress-fill" style="width:65%;"></div>
    </div>
    <p style="font-size:12px;color:#6f6f6f;margin-top:.4rem;">65% complete</p>
  </div>

  <!-- ========================================================
    VIOLATION 12 (WARNING — WCAG 4.1.2):
    Modal dialog declared with role="dialog" but missing:
      - aria-labelledby (pointing to the dialog title)
      - aria-describedby (optional but best practice)
      - aria-modal="true"
    Without these, screen readers won't announce the dialog
    title when it opens, leaving users disoriented.
    BOB SHOULD FIX:
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
  ========================================================= -->
  <div class="modal-overlay" id="edit-modal">
    <div class="modal" role="dialog">
      <!-- ====================================================
        VIOLATION 13 (CRITICAL — WCAG 4.1.2):
        Modal close button contains only an "×" character.
        This is unreliable across different screen readers.
        BOB SHOULD FIX: aria-label="Close edit product dialog"
      ===================================================== -->
      <button onclick="closeModal()" style="position:absolute;top:12px;right:12px;background:none;border:none;font-size:20px;cursor:pointer;color:#6f6f6f;">×</button>

      <h3 id="modal-title" style="margin-bottom:1.25rem;">Edit Product</h3>

      <div style="display:flex;flex-direction:column;gap:1rem;">
        <div>
          <label for="edit-name" style="font-size:12px;font-weight:600;display:block;margin-bottom:.3rem;">Product Name</label>
          <input type="text" id="edit-name" value="Wireless Headphones Pro">
        </div>
        <div>
          <label for="edit-price" style="font-size:12px;font-weight:600;display:block;margin-bottom:.3rem;">Price (USD)</label>
          <input type="number" id="edit-price" value="149.99" step="0.01">
        </div>
        <!-- ====================================================
          VIOLATION 14 (CRITICAL — WCAG 4.1.2):
          Password field inside the modal for "Admin Override"
          has NO associated label. Only placeholder text present.
          BOB SHOULD FIX:
            <label for="admin-override">Admin password to confirm changes</label>
            <input type="password" id="admin-override" aria-label="Admin password to confirm changes">
        ===================================================== -->
        <div>
          <input type="password" id="admin-override" placeholder="Admin password to confirm">
        </div>
        <div style="display:flex;gap:.75rem;justify-content:flex-end;margin-top:.5rem;">
          <button class="btn btn-ghost" onclick="closeModal()">Cancel</button>
          <button class="btn btn-primary" onclick="saveProduct()">Save Changes</button>
        </div>
      </div>
    </div>
  </div>

</div><!-- end .container -->

<script>
function filterProducts(v) { console.log('filtering:', v); }
function openFilters() { console.log('filters opened'); }
function openNotifications() { console.log('notifications opened'); }
function editProduct(id) { document.getElementById('edit-modal').classList.add('open'); }
function deleteProduct(id) { if(confirm('Delete product ' + id + '?')) console.log('deleted', id); }
function closeModal() { document.getElementById('edit-modal').classList.remove('open'); }
function saveProduct() { console.log('saved'); closeModal(); }
function handleUpload(input, id) {
  document.getElementById('upload-progress').style.display = 'block';
  let p = 0;
  const fill = document.getElementById('progress-fill');
  const iv = setInterval(() => {
    p += Math.random() * 20;
    if (p >= 100) { p = 100; clearInterval(iv); }
    fill.style.width = Math.round(p) + '%';
  }, 300);
}
</script>
</body>
</html>
