document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) window.lucide.createIcons();

  const menuButton = document.querySelector(".menu-button");
  const navigation = document.querySelector(".site-navigation");

  if (!menuButton || !navigation) return;

  const closeMenu = () => {
    navigation.classList.remove("is-open");
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", document.documentElement.lang === "ko" ? "메뉴 열기" : "Open navigation");
    menuButton.innerHTML = '<i data-lucide="menu"></i>';
    if (window.lucide) window.lucide.createIcons();
  };

  menuButton.addEventListener("click", () => {
    const open = !navigation.classList.contains("is-open");
    navigation.classList.toggle("is-open", open);
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute("aria-label", open
      ? (document.documentElement.lang === "ko" ? "메뉴 닫기" : "Close navigation")
      : (document.documentElement.lang === "ko" ? "메뉴 열기" : "Open navigation"));
    menuButton.innerHTML = `<i data-lucide="${open ? "x" : "menu"}"></i>`;
    if (window.lucide) window.lucide.createIcons();
  });

  navigation.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
  window.addEventListener("resize", () => {
    if (window.innerWidth > 760) closeMenu();
  });
});
